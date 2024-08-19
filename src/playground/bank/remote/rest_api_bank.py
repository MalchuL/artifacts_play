import logging
from typing import Dict, List, Optional

from src.playground.bank.bank import Bank

from src.playground.items.item import Item, Items
from src.rest_api_client.api.bank import GetBankItems, GetBankGolds, GetBankItem
from src.rest_api_client.client import AuthenticatedClient
from src.rest_api_client.errors import ArtifactsHTTPStatusError
from src.rest_api_client.model import SimpleItemSchema, DataPageSimpleItemSchema

logger = logging.getLogger(__name__)


class RestApiBank(Bank):

    def __init__(self, client: AuthenticatedClient):
        super().__init__()

        # Hidden variables
        self._client = client

    def __parse_items(self, schema: SimpleItemSchema) -> Items:
        return Items(Item(schema.code), quantity=schema.quantity)

    def get_bank_items(self) -> Dict[str, Items]:
        date_page_items: DataPageSimpleItemSchema = GetBankItems(page=1, client=self._client)()
        total_pages = date_page_items.pages
        schemas: List[SimpleItemSchema] = list(date_page_items.data)

        for page in range(2, total_pages + 1):
            date_page_items: DataPageSimpleItemSchema = GetBankItems(page=page,
                                                                     client=self._client)()
            schemas.extend(date_page_items.data)

        items = {}
        for item_schema in schemas:
            parsed_item = self.__parse_items(item_schema)
            if parsed_item.item.code in items:
                raise KeyError(
                    f"{parsed_item.item.code}:{items[parsed_item.item.code]}\n {parsed_item} already defined"
                    f" for object. they are equal={items[parsed_item.item.code] == parsed_item}")
            items[parsed_item.item.code] = parsed_item

        return items

    def get_bank_item(self, item: Item) -> Optional[Items]:
        try:
            quantity = GetBankItem(code=item.code, client=self._client)().quantity
            return Items(item=item, quantity=quantity)
        except ArtifactsHTTPStatusError as e:
            if e.status_code == 404:
                return None
            else:
                raise


    def get_bank_gold(self) -> int:
        gold = GetBankGolds(client=self._client)().data.quantity
        return gold
