from typing import List, Dict, Optional

from src.playground.items import Items, Item
from .character_task import CharacterTask


class AvailableItems(CharacterTask):
    def __init__(self, char_name: str, required_items: Optional[List[Item]] = None):

        super().__init__(char_name)
        self.required_items = required_items

    def all_items(self, char_name) -> Dict[str, Items]:
        items: Dict[str, Items] = {}
        world = self.world
        bank = world.bank
        bank_items = bank.get_bank_items()
        for item in bank_items:
            items[item.item.code] = item
        character = world.get_character(char_name)
        character_items = character.inventory.items
        for item in character_items:
            item_code = item.item.code
            if item.item.code in items:
                items[item_code] = Items(item=item.item,
                                         quantity=item.quantity + items[item_code].quantity)
            else:
                items[item_code] = item
        return items

    def filtered_items(self, char_name, filter_items: List[Item]):
        # TODO rewrite on optimized version
        items = self.all_items(char_name=char_name)
        filtered_items = {}
        for filter_item in filter_items:
            if filter_item.code in items:
                filtered_items[filter_item.code] = items[filter_item.code]
        return filtered_items

    def find_all_items(self, char_name: str,
                       required_items: Optional[List[Item]] = None):
        if required_items:
            filter_items = required_items
            self.logger.info(f"Search available items in list {required_items}")
            out_items = self.filtered_items(char_name, filter_items)
        else:
            self.logger.info(f"Search available items")
            out_items = self.all_items(char_name)

        items = list(out_items.values())
        self.logger.info(f"Available items, {items}")
        self.logger.info(f"End search items")
        self.outputs()["available_items"] = items

    def run(self):
        return self.find_all_items(char_name=self.char_name, required_items=self.required_items)
