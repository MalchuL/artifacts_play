from src.player.strategy.utils.items import merge_items
from src.playground.items import Items, Item


def test_merge_items():
    item1_list = [Items(Item("item1"), 1), Items(Item("item2"), 2)]
    item2_list = [Items(Item("item3"), 1), Items(Item("item2"), 2)]
    print(merge_items(item1_list, item2_list))