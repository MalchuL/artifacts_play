import logging
from typing import Optional, List, Dict

from src.playground.characters.remote.errors import char_exception_handler
from src.playground.characters.remote.internal_message import InternalCharacterMessage
from src.playground.characters.inventory import Inventory, EquipmentSlot
from src.playground.constants import MAX_CONSUMABLES_EQUIPPED
from src.playground.items.item import Item, Items
from src.rest_api_client.api.my_characters import ActionEquipItem, ActionDeleteItem, \
    ActionUnequipItem
from src.rest_api_client.client import AuthenticatedClient
from src.rest_api_client.model import CharacterSchema, EquipSchema, Slot, EquipmentResponseSchema, \
    UnequipSchema, SimpleItemSchema, DeleteItemResponseSchema

logger = logging.getLogger(__name__)


class RemoteInventory(Inventory):
    def __init__(self, char_message: InternalCharacterMessage):
        self.__state = char_message

    @property
    def equipment(self) -> Dict[EquipmentSlot, Optional[Items]]:
        state = self._state
        equipment = {}
        for slot in Slot:
            item_code = getattr(state, slot.value + "_slot")
            if slot in [Slot.consumable1, slot.consumable2]:
                quantity = getattr(state, slot.value + "_slot_quantity")
            else:
                quantity = 1
            if item_code:
                item = Item(code=item_code)
                equipment[EquipmentSlot(slot.value)] = Items(item, quantity=quantity)
        return equipment

    @property
    def consumables_amount(self) -> Dict[EquipmentSlot, Items]:
        state = self._state
        consumables = {}
        for slot in [Slot.consumable1, Slot.consumable2]:
            item_code = getattr(state, slot.value + "_slot")
            quantity = getattr(state, slot.value + "_slot_quantity")
            if item_code and quantity:
                item = Items(Item(code=item_code), quantity=quantity)
                consumables[EquipmentSlot(slot.value)] = item
        return consumables

    @property
    def name(self) -> str:
        return self.__state.name

    @property
    def _client(self) -> AuthenticatedClient:
        return self.__state.client

    @property
    def _state(self) -> CharacterSchema:
        return self.__state.char_schema

    @_state.setter
    def _state(self, state: CharacterSchema):
        self.__state.char_schema = state

    @property
    def items(self) -> List[Items]:
        items_list = []
        for items in sorted(self._state.inventory, key=lambda schema_items: schema_items.slot):
            if items.quantity > 0:
                items_list.append(Items(item=Item(items.code), quantity=items.quantity))
        return items_list

    @property
    def max_inventory_amount(self) -> int:
        return self._state.inventory_max_items

    @property
    def capacity(self) -> int:
        return len(self._state.inventory)

    @char_exception_handler
    def equip_item(self, item: Item, item_slot: EquipmentSlot, count: int = 1):
        count = min(count, MAX_CONSUMABLES_EQUIPPED)
        equip = EquipSchema(code=item.code, slot=Slot(item_slot.value), quantity=count)
        equip_call = ActionEquipItem(name=self.name, client=self._client)
        result: EquipmentResponseSchema = equip_call(equip)
        self._state = result.data.character
        logger.debug(f"Equip results: {result.data.slot}, {result.data.item}")

    @char_exception_handler
    def unequip_item(self, item_slot: EquipmentSlot, count: int = 1):
        count = min(count, MAX_CONSUMABLES_EQUIPPED)
        unequip = UnequipSchema(slot=Slot(item_slot.value), quantity=count)
        unequip_call = ActionUnequipItem(name=self.name, client=self._client)
        result: EquipmentResponseSchema = unequip_call(unequip)
        self._state = result.data.character
        logger.debug(f"Unequip results: {result.data.slot}, {result.data.item}")

    @char_exception_handler
    def delete_item(self, item: Item, amount: int):
        delete = SimpleItemSchema(code=item.code, quantity=amount)
        delete_call = ActionDeleteItem(name=self.name, client=self._client)
        result: DeleteItemResponseSchema = delete_call(delete)
        self._state = result.data.character
        logger.debug(f"Delete item results: {result.data.item}, {result.data.character.inventory}")
