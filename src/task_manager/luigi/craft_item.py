import json
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
from src.task_manager.luigi.adapters import ItemsAdapter, ListItemsAdapter, to_json, from_json, \
    ListItemAdapter
from src.task_manager.luigi.available_items import AvailableItems
from src.task_manager.luigi.character_task import CharacterTask
from src.task_manager.luigi.deposit_items import BankTask
from src.task_manager.luigi.gather_items import HarvestItemsTask
from src.task_manager.luigi.hunt_task import HuntTask

from src.task_manager.luigi.utils import log_job

logger = logging.getLogger(__name__)


class CraftItemTask(CharacterTask):
    crating_items: ItemsAdapter = luigi.DictParameter(
        schema=ItemsAdapter.json_schema())  # Item wanted to craft

    def requires(self):
        crating_item = from_json(self.crating_items, ItemsAdapter)
        world = self.world

        crafting_items = world.crafting.get_craft(crating_item.item)
        items = crafting_items.craft.items
        whole_items = to_json([item.item for item in items], ListItemAdapter)

        return AvailableItems(char_name=self.char_name,
                              required_items=whole_items,
                              datetime=self.datetime)  # Don't use now inside requires

    def run(self):
        crafting_items: Items = from_json(self.crating_items, ItemsAdapter)
        world = self.world
        log_job(f"Try to create it={crafting_items}", logger)
        with self.input().open("r") as f:
            available_items = from_json(json.load(f), ListItemsAdapter)
            available_items_dict: Dict[str, Items] = {items.item.code: items for items
                                                                 in available_items}
        item_schema = world.crafting.get_craft(crafting_items.item)
        required_items = item_schema.craft.items
        missed_items = []
        for required_item in required_items:
            available_quantity = available_items_dict[required_item.item.code].quantity
            required_quantity = required_item.quantity * crafting_items.quantity
            if available_quantity < required_quantity:
                missed_items.append(Items(item=required_item.item,
                                          quantity=required_quantity - available_quantity))
        if missed_items:
            logger.info(f"There are missed items {missed_items} to create {crafting_items}")
            from src.task_manager.luigi.get_items_task import GetItemsTask
            now_time = datetime.now()
            yield [GetItemsTask(items=missed_item, char_name=self.char_name, datetime=now_time) for
                   missed_item in missed_items]

        map_finder = MapFinder(world)
        _items = item_schema.craft.items
        character = world.get_character(self.char_name)
        inventory_capacity = character.inventory.max_inventory_amount


        crafted_items = 0
        required_amount = sum(item.quantity for item in withdraw_items)
        crafting_amount = inventory_capacity // required_amount
        target_amount = crating_item.quantity
        log_job(logger, f"Start creating items {crating_item.item.code}={crating_item.quantity}")
        logger.info(
            f"Number of steps={(target_amount + crafting_amount - 1) // crafting_amount}, {self.datetime}")

        for i in range((target_amount + crafting_amount - 1) // crafting_amount):
            total_amount = (i + 1) * crafting_amount
            amount = crafting_amount
            logger.info(f"Try to create target items={Items(crating_item.item, amount)}")

            if total_amount > target_amount:
                amount = crafting_amount - (total_amount - target_amount)

            batch_items = [Items(item.item, item.quantity * amount)
                           for item in withdraw_items]

            bank_items_schema = to_json(batch_items, ListItemsAdapter)
            bank_task = BankTask(withdraw_items=bank_items_schema, char_name=self.char_name,
                                 deposit_all_items=True, datetime=datetime.now())
            yield luigi.DynamicRequirements(bank_task)
            logger.info(f"Finding workwhop")

            skill2building = {SkillType.WEAPON_CRAFTING: BuildingType.WEAPON_CRAFTING_WORKSHOP,
                              SkillType.GEAR_CRAFTING: BuildingType.GEAR_CRAFTING_WORKSHOP,
                              SkillType.JEWERLY_CRAFTING: BuildingType.JEWERLY_CRAFTING_WORKSHOP,
                              SkillType.COOKING: BuildingType.COOKING,
                              SkillType.WOODCUTTING: BuildingType.WOODCUTTING,
                              SkillType.MINING: BuildingType.MINING,
                              }
            building_type = skill2building[crafting_schema.craft.skill]
            workshop_location = map_finder.find_building(building_type=building_type)[0]
            logger.info(f"Found workshop {workshop_location}")
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
