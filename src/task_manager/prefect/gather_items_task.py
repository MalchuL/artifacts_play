from prefect import flow

from .craft_item import PrefectCraftItemsTask
from .harvest_items import PrefectHarvestItemsTask
from .hunt_items import PrefectHuntItemsTask
from ..workflows.adapters import ItemsAdapter, from_json, to_json
from ..workflows.gather_items_task import GatherItemsTask
from ...playground.items import Items


class PrefectGatherItemsTask(GatherItemsTask):

    def harvest_task(self, char_name: str, items: Items):
        task = PrefectHarvestItemsTask(char_name=char_name, items=items)
        task.start()

    def hunt_task(self, char_name: str, items: Items):
        task = PrefectHuntItemsTask(char_name=char_name, items=items)
        task.start()

    def craft_task(self, char_name: str, items: Items):
        task = PrefectCraftItemsTask(char_name=char_name, items=items)
        task.start()

    def run(self):
        @flow(name="gather_items", log_prints=True)
        def _gather_items(char_name: str, items: ItemsAdapter.core_schema):
            return self.gather_items(char_name=char_name,
                                     items=from_json(items, ItemsAdapter))

        return _gather_items(char_name=self.char_name,
                             items=to_json(self.items, ItemsAdapter))
