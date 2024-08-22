from typing import Optional, Dict

from prefect import flow, task

from src.task_manager.workflows.adapters import ListItemAdapter, from_json, to_json
from src.task_manager.workflows.available_items import AvailableItems


class PrefectAvailableItems(AvailableItems):

    def run(self):
        @task(name="find_all_items", log_prints=True)
        def _find_all_items(char_name: str, required_items: ListItemAdapter.core_schema):
            return self.find_all_items(char_name=char_name,
                                       required_items=from_json(required_items, ListItemAdapter))

        return _find_all_items(char_name=self.char_name,
                               required_items=to_json(self.required_items, ListItemAdapter))
