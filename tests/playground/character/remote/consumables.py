from src.playground.items import Item


def test_use_consumable(character):
    character.wait_until_ready()
    character.inventory.use_item(Item("cooked_gudgeon"), 1)
