from typing import Dict, Optional, List

from src.playground.characters import Inventory, EquipmentSlot
from src.playground.items import Item, Items


class ProxyInventory(Inventory):

    def __init__(self, equipment: Dict[EquipmentSlot, Optional[Item]]):
        self._equipment = equipment

    @property
    def items(self) -> List[Items]:
        raise NotImplementedError

    @property
    def equipment(self) -> Dict[EquipmentSlot, Optional[Item]]:
        return self._equipment

    @property
    def consumables_amount(self) -> Dict[EquipmentSlot, Items]:
        consumables = {}
        equipment = self.equipment
        for slot in [EquipmentSlot.CONSUMABLE1, EquipmentSlot.CONSUMABLE2]:
            if slot in equipment:
                consumables[slot] = Items(equipment[slot], quantity=100)
        return consumables

    @property
    def max_inventory_amount(self) -> int:
        raise NotImplementedError

    @property
    def capacity(self) -> int:
        raise NotImplementedError

    def equip_item(self, item: Item, item_slot: EquipmentSlot):
        raise NotImplementedError

    def unequip_item(self, item_slot: EquipmentSlot):
        raise NotImplementedError

    def delete_item(self, item: Item, amount: int):
        raise NotImplementedError
