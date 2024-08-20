from .character_task import CharacterTask
from .craft_item import CraftItemsTask
from .harvest_items import HarvestItemsTask
from .hunt_task import HuntItemsTask
from ...playground.items import Items
from ...playground.utilites.items_finder import ItemFinder


class GatherItemsTask(CharacterTask):

    def __init__(self, char_name: str, items: Items):
        super().__init__(char_name)
        self.items = items

    def harvest_task(self, char_name: str, items: Items):
        task = HarvestItemsTask(char_name=char_name, items=items)
        task.start()

    def hunt_task(self, char_name: str, items: Items):
        task = HuntItemsTask(char_name=char_name, items=items)
        task.start()

    def craft_task(self, char_name: str, items: Items):
        task = CraftItemsTask(char_name=char_name, items=items)
        task.start()

    def gather_items(self, char_name: str, items: Items):
        world = self.world
        finder = ItemFinder(world)

        if finder.find_item_in_resources(search_item=items.item):
            self.logger.info(f"Try to HARVEST resource={items}")
            self.harvest_task(char_name=char_name, items=items)
        elif finder.find_item_in_monsters(search_item=items.item):
            self.logger.info(f"Try to HUNT resource={items}")
            self.hunt_task(char_name=char_name, items=items)
        elif finder.find_item_in_crafts(search_item=items.item):
            self.logger.info(f"Try to CRAFT resource={items}")
            self.craft_task(char_name=char_name, items=items)
        else:
            raise ValueError(f"Can't find any type of gathering resource={items.item}")

    def run(self):
        return self.gather_items(char_name=self.char_name, items=self.items)
