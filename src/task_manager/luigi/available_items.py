import json
import logging
import os
import pickle
from datetime import datetime
from typing import List, Dict

import luigi
from dynaconf import settings
from luigi.format import Nop
from luigi.freezing import recursively_unfreeze

from src.playground.fabric.playground_world import PlaygroundWorld
from src.playground.items import Items, Item
from src.playground.utilites.items_finder import ItemFinder
from src.task_manager.luigi.adapters import ListItemsAdapter, from_json, ListItemAdapter, to_json
from src.task_manager.luigi.character_task import CharacterTask
from src.task_manager.luigi.state import get_world
from src.task_manager.luigi.utils import log_job

logger = logging.getLogger(__name__)


class AvailableItems(CharacterTask):
    required_items: List[Item] = luigi.OptionalListParameter(default=None,
                                                             schema=ListItemAdapter.json_schema())

    output_extension = "json"

    def all_items(self) -> Dict[str, Items]:
        items: Dict[str, Items] = {}
        world = self.world
        bank = world.bank
        bank_items = bank.get_bank_items()
        for item in bank_items:
            items[item.item.code] = item
        character = world.get_character(self.char_name)
        character_items = character.inventory.items
        for item in character_items:
            item_code = item.item.code
            if item.item.code in items:
                items[item_code] = Items(item=item.item,
                                         quantity=item.quantity + items[item_code].quantity)
            else:
                items[item_code] = item
        return items

    def filtered_items(self, filter_items: List[Item]):
        # TODO rewrite on optimized version
        items = self.all_items()
        filtered_items = {}
        for filter_item in filter_items:
            if filter_item.code in items:
                filtered_items[filter_item.code] = items[filter_item.code]
        return filtered_items

    def run(self):
        if self.required_items:
            filter_items = from_json(self.required_items, ListItemAdapter)
            log_job(f"Search available items in list {self.required_items}", logger)
            out_items = self.filtered_items(filter_items)
        else:
            log_job(f"Search available items", logger)
            out_items = self.all_items()

        items = list(out_items.values())
        logger.info(f"Available items, {items}")
        log_job(f"End search items", logger)
        with self.output().open("w") as f:
            json.dump(to_json(items, ListItemsAdapter), f)
