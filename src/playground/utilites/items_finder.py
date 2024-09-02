from typing import Optional, List, Dict

from src.playground.bank import Bank
from src.playground.characters import Character
from src.playground.fabric.playground_world import PlaygroundWorld
from src.playground.items import Item, Items, ItemCraftingInfoManager
from src.playground.items.crafting import CraftingItem
from src.playground.monsters import DetailedMonster
from src.playground.resources import Resource


class ItemFinder:
    def __init__(self, world: PlaygroundWorld):
        self.world = world

    @staticmethod
    def find_item_on_character(character: Character, search_item: Item) -> Optional[Items]:
        assert isinstance(search_item, Item)
        character_items: List[Items] = character.inventory.items
        item2char_items: Dict[str, Items] = {items.item.code: items for items in character_items}
        return item2char_items.get(search_item.code, None)

    def find_item_in_bank(self, search_item: Item) -> Optional[Items]:
        assert isinstance(search_item, Item)
        bank: Bank = self.world.bank
        bank_items = bank.get_bank_item(search_item)
        return bank_items

    def find_item_in_crafts(self, search_item: Item) -> Optional[CraftingItem]:
        """
        Finds items only if they can be crafted
        :param search_item:
        :return:
        """
        assert isinstance(search_item, Item)
        crafting: ItemCraftingInfoManager = self.world.item_details
        crafts = {item.code: item for item in crafting.get_crafts() if item.craft}
        return crafts.get(search_item.code, None)

    def find_item_in_monsters(self, search_item: Item) -> List[DetailedMonster]:
        assert isinstance(search_item, Item)
        monsters_manager = self.world.monsters
        monster2drops = {monster.code: monster.drops for monster in monsters_manager.monsters}
        monsters_has_drops: List[DetailedMonster] = []
        for monster_code, drops in monster2drops.items():
            for drop in drops:
                if drop.item.code == search_item.code:
                    monster = monsters_manager.monster_from_id(monster_code)
                    monsters_has_drops.append(monsters_manager.get_monster_info(monster))
        return monsters_has_drops

    def find_item_in_resources(self, search_item: Item) -> List[Resource]:
        assert isinstance(search_item, Item)
        resources_manager = self.world.resources
        resource2drops = {resource.code: resource.drops for resource in
                          resources_manager.resources}
        resource_has_drops: List[Resource] = []
        for resource_code, drops in resource2drops.items():
            for drop in drops:
                if drop.item.code == search_item.code:
                    resource = resources_manager.get_resource_info(resource_code)
                    resource_has_drops.append(resource)
        return resource_has_drops
