from typing import List

from prefect import flow, task

from src.playground.items import Items, Item
from .available_items import PrefectAvailableItems
from .deposit_items import PrefectBankTask
from ..workflows.adapters import ItemsAdapter, from_json, to_json
from ..workflows.craft_item import CraftItemsTask


class PrefectCraftItemsTask(CraftItemsTask):
    @staticmethod
    def available_items_task(char_name, required_items: List[Item]):
        task = PrefectAvailableItems(char_name=char_name,
                              required_items=required_items)
        output = task.start()
        return output["available_items"]

    @staticmethod
    def gather_items_task(char_name, items: Items):
        from src.task_manager.prefect.gather_items_task import PrefectGatherItemsTask
        task = PrefectGatherItemsTask(char_name=char_name, items=items)
        task.start()

    @staticmethod
    def bank_items_task(char_name, items: List[Items]):
        task = PrefectBankTask(char_name=char_name, deposit_all_items=True, withdraw_items=items)
        task.start()

    def run(self):
        @task(name="craft_item", log_prints=True)
        def _craft_item(char_name: str, crafting_items: ItemsAdapter.core_schema):
            return self.craft_item(char_name=char_name,
                                   crafting_items=from_json(crafting_items, ItemsAdapter))

        return _craft_item(char_name=self.char_name,
                           crafting_items=to_json(self.items, ItemsAdapter))
