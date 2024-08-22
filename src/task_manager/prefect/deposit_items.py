from prefect import flow, task

from ..workflows.adapters import ListItemsAdapter, from_json, to_json
from ..workflows.deposit_items import BankTask


class PrefectBankTask(BankTask):

    def run(self):
        @task(name="deposit_withdraw_bank", log_prints=True)
        def _deposit_withdraw_bank(char_name: str,
                                   deposit_items: ListItemsAdapter.core_schema = None,
                                   deposit_gold: int = 0,
                                   deposit_all_items: bool = False,
                                   withdraw_items: ListItemsAdapter.core_schema = None,
                                   withdraw_gold: int = 0):
            deposit_items: ListItemsAdapter = from_json(deposit_items, ListItemsAdapter)
            withdraw_items: ListItemsAdapter = from_json(withdraw_items, ListItemsAdapter)
            return self.deposit_withdraw_bank(char_name=char_name,
                                              deposit_items=deposit_items,
                                              deposit_gold=deposit_gold,
                                              deposit_all_items=deposit_all_items,
                                              withdraw_items=withdraw_items,
                                              withdraw_gold=withdraw_gold)

        return _deposit_withdraw_bank(char_name=self.char_name,
                                      deposit_items=to_json(self.deposit_items,
                                                            ListItemsAdapter),
                                      deposit_gold=self.deposit_gold,
                                      deposit_all_items=self.deposit_all_items,
                                      withdraw_items=to_json(self.withdraw_items,
                                                             ListItemsAdapter),
                                      withdraw_gold=self.withdraw_gold)
