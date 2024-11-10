import copy
from typing import Dict, List, Optional

from src.playground.characters import SkillType, EquipmentSlot, Character
from src.playground.items import Items, Item, ItemType
from src.playground.utilites.map_finder import MapFinder, BuildingType
from .available_items import AvailableItems
from .character_task import CharacterTask
from .deposit_items import BankTask
from .gather_items_task import GatherItemsTask
from .task import Rerun
from ...playground.errors import CharacterInventoryFullException
from ...playground.items.crafting import ItemDetails


class EquipItemTask(CharacterTask):
    def __init__(self, char_name: str, equipped_item: Item,
                 equipment_slot: Optional[EquipmentSlot] = None):
        super().__init__(char_name)
        self.equipped_item = equipped_item
        self.equipment_slot = equipment_slot

    @staticmethod
    def gather_items_task(char_name, items: Items):
        task = GatherItemsTask(char_name=char_name, items=items)
        task.start()

    @staticmethod
    def bank_items_task(char_name, items: List[Items]):
        task = BankTask(char_name=char_name, deposit_all_items=True, withdraw_items=items)
        task.start()

    def find_equip_slot(self, character: Character, item: ItemDetails) -> EquipmentSlot:
        inventory = character.inventory
        equipment = inventory.equipment
        if item.type == ItemType.ring:
            if equipment.get(EquipmentSlot.RING1, None) is None:
                slot = EquipmentSlot.RING1
            else:
                slot = EquipmentSlot.RING2
        elif item.type == ItemType.artifact:
            if equipment.get(EquipmentSlot.ARTIFACT1, None) is None:
                slot = EquipmentSlot.ARTIFACT1
            elif equipment.get(EquipmentSlot.ARTIFACT2, None) is None:
                slot = EquipmentSlot.ARTIFACT2
            else:
                slot = EquipmentSlot.ARTIFACT3
        elif item.type == ItemType.utility:
            if equipment.get(EquipmentSlot.UTILITY1, None) is None:
                slot = EquipmentSlot.UTILITY1
            else:
                slot = EquipmentSlot.UTILITY2
        else:
            slot = EquipmentSlot(item.type.value)
        return slot

    def equip_item(self, char_name, equip_item: Item, slot: Optional[EquipmentSlot] = None):
        self.logger.info(f"Try to equip {equip_item}")

        world = self.world
        bank = world.bank

        character = world.get_character(char_name)
        inventory_item = character.inventory.get_items(equip_item)

        item_details: ItemDetails = world.item_details.get_item(equip_item)
        if slot is None:
            slot = self.find_equip_slot(character, item_details)
        if character.inventory.equipment.get(slot, None) is not None:
            equiped_item = character.inventory.equipment[slot]
            if equiped_item.code == equip_item.code:
                self.logger.info(f"{equiped_item} is already equiped in {slot}")
                return

        if inventory_item is None:
            bank_item = bank.get_bank_item(equip_item)
            if bank_item is not None:
                self.bank_items_task(char_name=char_name, items=[Items(equip_item, quantity=1)])

        is_equipped = False

        if inventory_item is not None:

            equipment = character.inventory.equipment
            if equipment.get(slot, None) is not None:
                character.wait_until_ready()
                try:
                    character.inventory.unequip_item(slot)
                except CharacterInventoryFullException as e:
                    self.bank_items_task(char_name, items=[Items(equip_item, quantity=1)])

            character.wait_until_ready()
            character.inventory.equip_item(equip_item, slot)
            character.wait_until_ready()

            is_equipped = True

        if not is_equipped:
            self.logger.info(
                f"Failed to equip item={equip_item} from {character.inventory.items} inventory")
            self.gather_items_task(char_name=char_name, items=Items(item=equip_item, quantity=1))
            raise Rerun("We have to gather items and try equip it again")
        else:
            self.logger.info(f"Successfully equiped {equip_item} in {slot}")

    def run(self):
        return self.equip_item(self.char_name, equip_item=self.equipped_item,
                               slot=self.equipment_slot)
