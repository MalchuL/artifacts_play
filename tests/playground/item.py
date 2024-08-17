from src.playground.items.item import Item, ItemType


def test_item():
    item1_type = ItemType.WEAPON
    item2_type = ItemType.WEAPON
    name = "item"
    item1 = Item(item1_type, name)
    item2 = Item(item2_type, name)
    assert item1 == item2
    item3_type = ItemType.EQUIPMENT
    item3 = Item(item3_type, name)
    assert item1 != item3
