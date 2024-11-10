from src.playground.characters import EquipmentSlot
from src.playground.items import Item


def test_character_move(character):
    character.wait_until_ready()
    character.move(0,0)
    character.wait_until_ready()
    character.move(1,1)

