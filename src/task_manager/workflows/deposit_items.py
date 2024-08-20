from typing import List

from src.playground.items import Items
from src.playground.utilites.map_finder import MapFinder, BuildingType
from .character_task import CharacterTask


class BankTask(CharacterTask):

    def __init__(self, char_name: str, deposit_items: List[Items] = None, deposit_gold=0,
                 deposit_all_items=False, withdraw_items: List[Items] = None, withdraw_gold=0):

        super().__init__(char_name)
        self.deposit_items = deposit_items
        self.deposit_gold = deposit_gold
        self.deposit_all_items = deposit_all_items
        self.withdraw_items = withdraw_items
        self.withdraw_gold = withdraw_gold

    def deposit_withdraw_bank(self, char_name: str,
                              deposit_items: List[Items] = None,
                              deposit_gold=0,
                              deposit_all_items=False,
                              withdraw_items: List[Items] = None,
                              withdraw_gold=0):
        world = self.world
        map_finder = MapFinder(world)
        bank_location = map_finder.find_building(BuildingType.BANK)[0]
        character = world.get_character(char_name)
        character.move(x=bank_location.x, y=bank_location.y)
        character.wait_until_ready()

        if deposit_items:
            for items in deposit_items:
                character.deposit_item(item=items.item, amount=items.quantity)
                character.wait_until_ready()
        if deposit_gold > 0:
            character.deposit_gold(amount=deposit_gold)
            character.wait_until_ready()
        if deposit_all_items:
            for items in character.inventory.items:
                character.deposit_item(item=items.item, amount=items.quantity)
                character.wait_until_ready()
        if withdraw_items:
            for items in withdraw_items:
                character.withdraw_item(item=items.item, amount=items.quantity)
                character.wait_until_ready()
        if withdraw_gold > 0:
            character.withdraw_gold(amount=withdraw_gold)
            character.wait_until_ready()

        self.logger.info(f"deposit_items={deposit_items}\n"
                         f"deposit_gold={deposit_gold}\n"
                         f"deposit_all_items={deposit_all_items}\n"
                         f"withdraw_items={withdraw_items}\n"
                         f"withdraw_gold={withdraw_gold}")

    def run(self):
        return self.deposit_withdraw_bank(char_name=self.char_name,
                                          deposit_items=self.deposit_items,
                                          deposit_gold=self.deposit_gold,
                                          deposit_all_items=self.deposit_all_items,
                                          withdraw_items=self.withdraw_items,
                                          withdraw_gold=self.withdraw_gold)
