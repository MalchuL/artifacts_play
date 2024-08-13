class ItemType:
    WEAPON = 1
    EQUIPMENT = 2
    CONSUMABLE = 3
    RESOURCE = 4
    BOOST = 5


class Item:
    def __init__(self, type: ItemType):
        self.type = type
