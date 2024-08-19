import logging
import os
import pickle
from datetime import datetime
from typing import List

import luigi
from dynaconf import settings
from luigi.format import Nop
from luigi.freezing import recursively_unfreeze

from src.playground.fabric.playground_world import PlaygroundWorld
from src.playground.items import Items, Item
from src.playground.utilites.items_finder import ItemFinder
from src.task_manager.luigi.adapters import ListItemsAdapter, from_json
from src.task_manager.luigi.state import get_world
from src.task_manager.luigi.utils import log_job

logger = logging.getLogger(__name__)


class FindMissedItems(luigi.Task):
    required_items: ListItemsAdapter = luigi.ListParameter()
    char_name: str = luigi.Parameter()
    datetime = luigi.DateSecondParameter(default=datetime.now(), interval=1)

    def run(self):
        required_items_list: ListItemsAdapter = from_json(self.required_items, ListItemsAdapter)
        world: PlaygroundWorld = get_world()
        missed_elements = []
        finder = ItemFinder(world)
        log_job(logger, "Finding required items")
        logger.info(f"Items to find {required_items_list}")
        for required_items in required_items_list:
            current_quantity = 0
            # Search items in bank
            bank_items = finder.find_item_in_bank(required_items.item)
            if bank_items is not None:
                current_quantity += bank_items.quantity
            # Search items on character
            character = world.get_character(self.char_name)
            character_items = finder.find_item_on_character(character, required_items.item)
            if character_items is not None:
                current_quantity += character_items.quantity
            # If we haven't enough items add as missed
            if current_quantity < required_items.quantity:
                quantity_diff = required_items.quantity - current_quantity
                missed_elements.append(Items(item=required_items.item, quantity=quantity_diff))
        logger.info(f"Missed items {missed_elements}")
        log_job(logger, "Missed ")
        with self.output().open("wb") as f:
            pickle.dump(missed_elements, f)

    def output(self):
        print("output datetime", str(self.datetime))
        return luigi.LocalTarget(
            os.path.join(settings.TASK_OUT_DIRECTORY,
                         f"{self.__class__.__name__}_{self.char_name}_{self.datetime}.pkl"),
            format=Nop)
