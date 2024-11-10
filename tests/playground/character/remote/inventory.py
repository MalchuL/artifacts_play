from src.playground.characters import EquipmentSlot
from src.playground.items import Item


def test_unequip(character):
    character.wait_until_ready()
    character.inventory.unequip_item(EquipmentSlot("weapon"))

def test_equip(character):
    character.wait_until_ready()
    character.inventory.equip_item(Item("wooden_stick"), EquipmentSlot("weapon"))

def test_inventory(character):
    character.wait_until_ready()
    print(character.inventory.free_amount)

def test_inventory(character):
    character.wait_until_ready()
    print(character.inventory.items)