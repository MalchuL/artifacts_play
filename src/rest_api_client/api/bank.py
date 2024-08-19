from typing import Union

from src.rest_api_client.api.named_classes import ObjectCodeRequest
from src.rest_api_client.client import Client, AuthenticatedClient
from src.rest_api_client.model import DataPageSimpleItemSchema, GoldBankResponseSchema, \
    SimpleItemSchema
from src.rest_api_client.requests.single_artifacts_request import SingleArtifactsRequest


class GetBankItems(SingleArtifactsRequest):
    """
    Get Bank Items
    Fetch all items in your bank.
    operationId: get_bank_items_my_bank_items_get
    """
    endpoint_pattern = '/my/bank/items'
    method_name = 'get'
    response_schema = DataPageSimpleItemSchema
    error_responses = {404: 'Items not found.'}

    def __call__(self) -> DataPageSimpleItemSchema:
        return super().__call__(None)


class GetBankItem(ObjectCodeRequest):
    """
    Get Bank Items
    Fetch all items in your bank.
    operationId: get_bank_items_my_bank_items_get
    """
    endpoint_pattern = '/my/bank/items?item_code={code}'
    method_name = 'get'
    response_schema = DataPageSimpleItemSchema
    error_responses = {404: 'Items not found.'}

    def __call__(self) -> SimpleItemSchema:
        schema: DataPageSimpleItemSchema = super().__call__(None)
        return schema.data[0]


class GetBankGolds(SingleArtifactsRequest):
    """
    Get Bank Golds
    Fetch golds in your bank.
    operationId: get_bank_golds_my_bank_gold_get
    """
    endpoint_pattern = '/my/bank/gold'
    method_name = 'get'
    response_schema = GoldBankResponseSchema
    error_responses = {}

    def __call__(self) -> GoldBankResponseSchema:
        return super().__call__(None)
