from prefect import flow, task

from .deposit_items import PrefectBankTask
from ..workflows.adapters import ItemsAdapter, from_json, to_json
from ..workflows.harvest_items import HarvestItemsTask
from ..workflows.hunt_task import HuntItemsTask


class PrefectHuntItemsTask(HuntItemsTask):

    @staticmethod
    def bank_items_task(char_name):
        task = PrefectBankTask(char_name=char_name, deposit_all_items=True)
        task.start()

    def run(self):
        @task(name="hunt_items", log_prints=True)
        def _hunt_items(char_name: str, items: ItemsAdapter.core_schema):
            return self.hunt_items(char_name=char_name,
                                   items=from_json(items, ItemsAdapter))

        return _hunt_items(char_name=self.char_name,
                           items=to_json(self.items, ItemsAdapter))
