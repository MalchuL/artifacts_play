import os
from datetime import datetime
from typing import List

import luigi
from dynaconf import settings

from src.playground.fabric.playground_world import PlaygroundWorld
from src.playground.items import Items
from src.playground.utilites.map_finder import MapFinder, BuildingType
from src.task_manager.luigi.adapters import ListItemsAdapter, from_json
from src.task_manager.luigi.state import get_world


class BankTask(luigi.Task):
    deposit_items: ListItemsAdapter = luigi.OptionalListParameter(default=None)
    deposit_gold: int = luigi.IntParameter(default=0)
    deposit_all_items: bool = luigi.BoolParameter(default=False)

    withdraw_items: ListItemsAdapter = luigi.OptionalListParameter(default=None)
    withdraw_gold: int = luigi.IntParameter(default=0)

    char_name: str = luigi.Parameter()
    datetime = luigi.DateSecondParameter(default=datetime.now(), interval=1)


    def run(self):
        world = get_world()
        map_finder = MapFinder(world)
        bank_location = map_finder.find_building(BuildingType.BANK)[0]
        character = world.get_character(self.char_name)
        character.move(x=bank_location.x, y=bank_location.y)
        character.wait_until_ready()

        if self.deposit_items:
            deposit_items: List[Items] = from_json(self.deposit_items, ListItemsAdapter)
            for items in deposit_items:
                character.deposit_item(item=items.item, amount=items.quantity)
                character.wait_until_ready()
        if self.deposit_gold > 0:
            character.deposit_gold(amount=self.deposit_gold)
            character.wait_until_ready()
        if self.deposit_all_items:
            for items in character.inventory.items:
                character.deposit_item(item=items.item, amount=items.quantity)
                character.wait_until_ready()
        if self.withdraw_items:
            withdraw_items: List[Items] = from_json(self.withdraw_items, ListItemsAdapter)
            for items in withdraw_items:
                character.withdraw_item(item=items.item, amount=items.quantity)
                character.wait_until_ready()
        if self.withdraw_gold > 0:
            character.withdraw_gold(amount=self.withdraw_gold)
            character.wait_until_ready()

        with self.output().open("w") as f:
            f.write(f"{self.deposit_items}, {self.deposit_gold}, {self.deposit_all_items}, {self.withdraw_items}, {self.withdraw_gold}")

    def output(self):
        return luigi.LocalTarget(
            os.path.join(settings.TASK_OUT_DIRECTORY,
                         f"{self.__class__.__name__}_{self.char_name}_{self.datetime}.txt"))

