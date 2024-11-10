from typing import Optional, List

from src.playground.characters import EquipmentSlot, Character
from src.playground.errors import CharacterInventoryFullException, ItemAlreadyEquippedException
from src.playground.fabric.playground_world import PlaygroundWorld
from src.playground.items import Items, Item, ItemType
from src.playground.items.crafting import ItemDetails
from ..character_strategy import CharacterStrategy
from ...players.player import Player
from ...task import TaskInfo, BankTask, BankObject, EquipTask


class EquipStrategyTask(CharacterStrategy):
    def __init__(self, player: Player, world: PlaygroundWorld, item: Item, amount: int = 1,
                 equipment_slot: Optional[EquipmentSlot] = None):
        super().__init__(player=player, world=world)
        self.equipped_item = item
        self.amount = amount
        self.equipment_slot = equipment_slot

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

    def unequip_item(self, character: Character, slot: EquipmentSlot):
        equipment = character.inventory.equipment
        if slot in equipment:
            items = equipment[slot]
            character.inventory.unequip_item(item_slot=slot, count=items.quantity)

    def equip_item(self, equip_item: Item, slot: Optional[EquipmentSlot] = None) -> List[TaskInfo]:
        self.logger.info(f"Try to equip {equip_item}")

        world = self.world

        character = self.player.character
        item_details: ItemDetails = world.item_details.get_item(equip_item)

        if slot is None:
            slot = self.find_equip_slot(character, item_details)

        # Check is item already equipped
        if character.inventory.equipment.get(slot, None) is not None:
            equipped_item = character.inventory.equipment[slot]
            if equipped_item.item.code == equip_item.code and equipped_item.quantity >= self.amount:
                self.logger.info(f"{equipped_item} is already equipped in {slot}")
                return []



        # Check is enough items on character
        inventory_items = character.inventory.get_items(equip_item)
        if inventory_items is None or inventory_items.quantity < self.amount:
            self.logger.info(f"Failed to equip {equip_item} in {slot}, deposit all items")
            bank_task = TaskInfo(bank_task=BankTask(deposit_all=True, withdraw=BankObject(
                items=[Items(equip_item, quantity=self.amount)])))
            equip_task = TaskInfo(
                equip_task=EquipTask(items=Items(equip_item, quantity=self.amount)))
            out_tasks = [equip_task, bank_task]
            return out_tasks

        # Unequip if it possible
        try:
            character.wait_until_ready()
            self.unequip_item(character, slot)
        except CharacterInventoryFullException as e:
            self.logger.info(f"Failed to unequip {equip_item} in {slot}, deposit all items")
            bank_task = TaskInfo(bank_task=BankTask(deposit_all=True, withdraw=BankObject(
                items=[Items(equip_item, quantity=self.amount)])))
            equip_task = TaskInfo(
                equip_task=EquipTask(items=Items(equip_item, quantity=self.amount)))
            out_tasks = [equip_task, bank_task]
            return out_tasks

        try:
            character.wait_until_ready()
            character.inventory.equip_item(equip_item, slot, count=self.amount)
        except ItemAlreadyEquippedException as e:
            self.logger.info(f"{equip_item} is already equipped in {slot}")
        character.wait_until_ready()
        self.logger.info(f"Successfully equiped {equip_item} in {slot}")
        return []

    def run(self) -> List[TaskInfo]:
        return self.equip_item(equip_item=self.equipped_item,
                               slot=self.equipment_slot)
