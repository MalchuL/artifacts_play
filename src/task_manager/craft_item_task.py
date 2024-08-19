import logging
from collections import deque
from typing import List, Union

import luigi

from src.playground.fabric.playground_world import PlaygroundWorld
from src.playground.items import Items, Item
from src.playground.items.crafting import CraftingItem, ItemDetails
from src.playground.utilites.items_finder import ItemFinder

logger = logging.getLogger(__name__)




class CreateItemTask(Task):
    def __init__(self, char_name, world: PlaygroundWorld):
        self.name = char_name
        self.world = world
        self.queue = deque()

    def item2str(self, item: Union[Item, CraftingItem, Items], quantity=None):
        if isinstance(item, ItemDetails):
            name = item.name
        else:
            if isinstance(item, Items):
                cur_item = item.item
            else:
                cur_item = item
            name = self.world.crafting.get_item(item=cur_item).name
        if quantity is not None:
            item = Items(item, quantity=quantity)
        if isinstance(item, Items):
            return f"{name}={item.quantity}"
        else:
            return name

    def log_job(self, job_text):
        string = "-" * 10
        string += f" {job_text} "
        string += "-" * 10
        logger.info(string)

    def __call__(self, crafted_items: Items):
        character = self.world.get_character(self.name)
        item_craft = self.world.crafting.get_craft(crafted_items.item)

        items_finder = ItemFinder(self.world)
        missing_items: List[Items] = []
        self.log_job("Start Required Items Search")
        logger.info(f"Required items {[self.item2str(item) for item in item_craft.craft.items]} "
                    f"to craft {self.item2str(item_craft)}")
        for required_items in item_craft.craft.items:
            required_items: Items
            req_item: Item = required_items.item
            self.log_job(f"Search for {self.item2str(required_items)}")

            required_quantity: int = required_items.quantity
            current_quantity = 0
            # Check character items

            # Check bank items
            if current_quantity < required_quantity:
                bank_items = self.world.bank.get_bank_item(req_item)
                bank_quantity = 0
                if bank_items is not None:
                    bank_quantity = bank_items.quantity
                    logger.info(f"Bank has {self.item2str(bank_items)} to "
                                f"craft {self.item2str(item_schema)}")
                current_quantity += bank_quantity
            logger.info(f"Char have {self.item2str(req_item, quantity=current_quantity)} to "
                        f"craft {self.item2str(item_schema)}")
            if current_quantity < required_quantity:
                missed_item = Items(req_item, required_quantity - current_quantity)
                missing_items.append(missed_item)
        logger.info(f"Character {character.name} need {list(map(self.item2str, missing_items))} "
                    f"to craft {self.item2str(item_schema)}")
        self.log_job("Finish Required Items Search")
