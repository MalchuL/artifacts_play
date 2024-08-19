import logging
import os
import pickle
from collections import deque
from datetime import datetime
from typing import List, Union, Dict

import luigi
from dynaconf import settings
from luigi.format import Nop
from luigi.freezing import recursively_unfreeze
from pydantic import TypeAdapter

from src.playground.characters import SkillType
from src.playground.fabric.playground_world import PlaygroundWorld
from src.playground.items import Items, Item
from src.playground.items.crafting import CraftingItem, ItemDetails
from src.playground.utilites.items_finder import ItemFinder
from src.playground.utilites.map_finder import MapFinder, BuildingType
from src.task_manager.luigi.adapters import ItemsAdapter, ListItemsAdapter, to_json, from_json
from src.task_manager.luigi.deposit_items import BankTask
from src.task_manager.luigi.gather_items import HarvestItemsTask
from src.task_manager.luigi.hunt_task import HuntTask
from src.task_manager.luigi.missed_items import FindMissedItems
from src.task_manager.luigi.state import get_world
from src.task_manager.luigi.utils import log_job

logger = logging.getLogger(__name__)


class CraftItemTask(luigi.Task):
    crating_item: ListItemsAdapter = luigi.DictParameter(
        schema=ItemsAdapter.json_schema())  # Item wanted to craft
    char_name: str = luigi.OptionalParameter()
    datetime = luigi.DateSecondParameter(default=datetime.now(), interval=1)

    def requires(self):
        crating_item = from_json(self.crating_item, ItemsAdapter)
        world = get_world()

        print(world, type(world), type(crating_item))
        item_craft = world.crafting.get_craft(crating_item.item)
        if item_craft.craft:
            items = item_craft.craft.items
            whole_items = to_json([Items(item.item, quantity=crating_item.quantity * item.quantity)
                for item in items], ListItemsAdapter)
            FindMissedItems.clear_instance_cache()
            return FindMissedItems(char_name=self.char_name,
                                   required_items=whole_items)

    def item2str(self, item: Union[Item, CraftingItem, Items], quantity=None):
        world = get_world()
        if isinstance(item, ItemDetails):
            name = item.name
        else:
            if isinstance(item, Items):
                cur_item = item.item
            else:
                cur_item = item
            name = world.crafting.get_item(item=cur_item).name
        if quantity is not None:
            item = Items(item, quantity=quantity)
        if isinstance(item, Items):
            return f"{name}={item.quantity}"
        else:
            return name

    def run(self):
        crating_item = from_json(self.crating_item, ItemsAdapter)
        world = get_world()
        log_job(logger, f"Try to create it={crating_item}")
        assert isinstance(crating_item, Items)
        with self.input().open("r") as f:
            required_items: List[Items] = pickle.load(f)
        logger.info(f"Required items {required_items}")
        if required_items:
            finder = ItemFinder(world)
            for required_item in required_items:
                # Because we have to create thoose amount of required items
                new_required_item = Items(item=required_item.item,
                                          quantity=required_item.quantity * crating_item.quantity)

                if finder.find_item_in_resources(search_item=required_item.item):
                    log_job(logger, f"Try to HARVEST resourse={required_item}")
                    new_harvest_item = to_json(new_required_item, ItemsAdapter)
                    yield HarvestItemsTask(items=new_harvest_item,
                                           char_name=self.char_name)
                    log_job(logger, f"END HARVEST resourse={required_item}")
                elif finder.find_item_in_monsters(search_item=required_item.item):
                    log_job(logger, f"Try to HUNT resourse={required_item}")
                    new_hunting_item = to_json(new_required_item, ItemsAdapter)
                    yield HuntTask(items=new_hunting_item,
                                   char_name=self.char_name)
                    log_job(logger, f"END HUNT resourse={required_item}")
                elif finder.find_item_in_crafts(search_item=required_item.item):
                    log_job(logger, f"Try to CRAFT resourse={required_item}")
                    new_crafting_items = to_json(new_required_item, ItemsAdapter)
                    yield CraftItemTask(crating_item=new_crafting_items, char_name=self.char_name)
                    log_job(logger, f"END CRAFTING resourse={required_item}")
                else:
                    raise ValueError(f"Can't find any type of gathering resourse={required_item}")

        map_finder = MapFinder(world)

        crafting_schema = world.crafting.get_craft(crating_item.item)
        withdraw_items = crafting_schema.craft.items

        character = world.get_character(self.char_name)
        inventory_capacity = character.inventory.max_inventory_amount
        crafted_items = 0
        required_amount = sum(item.quantity for item in withdraw_items)
        crafting_amount = inventory_capacity // required_amount
        target_amount = crating_item.quantity
        log_job(logger, f"Start creating items {crating_item.item.code}={crating_item.quantity}")
        logger.info(f"Number of steps={(target_amount + crafting_amount - 1) // crafting_amount}")

        for i in range((target_amount + crafting_amount - 1) // crafting_amount):
            total_amount = (i + 1) * crafting_amount
            amount = crafting_amount
            if total_amount > target_amount:
                amount = crafting_amount - (total_amount - target_amount)

            batch_items = [Items(item.item, item.quantity * amount)
                           for item in withdraw_items]

            bank_items_schema = to_json(batch_items, ListItemsAdapter)
            yield BankTask(withdraw_items=bank_items_schema, char_name=self.char_name,
                           deposit_all_items=True)

            skill2building = {SkillType.WEAPON_CRAFTING: BuildingType.WEAPON_CRAFTING_WORKSHOP,
                              SkillType.GEAR_CRAFTING: BuildingType.GEAR_CRAFTING_WORKSHOP,
                              SkillType.JEWERLY_CRAFTING: BuildingType.JEWERLY_CRAFTING_WORKSHOP,
                              SkillType.COOKING: BuildingType.COOKING,
                              SkillType.WOODCUTTING: BuildingType.WOODCUTTING,
                              SkillType.MINING: BuildingType.MINING,
                              }
            building_type = skill2building[crafting_schema.craft.skill]
            workshop_location = map_finder.find_building(building_type=building_type)[0]
            x, y = character.position
            if x != workshop_location.x or y != workshop_location.y:
                character.move(x=workshop_location.x, y=workshop_location.y)
            character.wait_until_ready()
            character.craft(recipe=crating_item.item, amount=amount)
            character.wait_until_ready()
            crafted_items += amount
        out_str = f"Finish Required Items Search, crafted items:{crating_item}={crafted_items}"
        log_job(logger, out_str)
        with self.output().open("wb") as f:
            f.write(out_str)

    def output(self):
        print("out char", self.char_name)
        print("out datetime", self.datetime)
        return luigi.LocalTarget(
            os.path.join(settings.TASK_OUT_DIRECTORY,
                         f"{self.__class__.__name__}_{self.char_name}_{self.datetime}.txt"))
