from typing import Union

from src.rest_api_client.api.named_classes import ObjectCodeRequest, PagedRequest
from src.rest_api_client.errors import ArtifactsHTTPStatusError
from src.rest_api_client.model import DataPageSimpleItemSchema, \
    SimpleItemSchema, BankResponseSchema
from src.rest_api_client.requests.single_artifacts_request import SingleArtifactsRequest


class GetBankDetails(SingleArtifactsRequest):
    """
    Get Bank Details
    Fetch bank details.
    operationId: get_bank_details_my_bank_get
    """
    endpoint_pattern = '/my/bank'
    method_name = 'get'
    response_schema = BankResponseSchema
    error_responses = {}

    def __call__(self) -> BankResponseSchema:
        return super().__call__(None)


class GetBankItems(PagedRequest):
    """
    Get Bank Items
    Fetch all items in your bank.
    operationId: get_bank_items_my_bank_items_get
    """
    endpoint_pattern = '/my/bank/items?page={page}&size={page_size}'
    method_name = 'get'
    response_schema = DataPageSimpleItemSchema
    error_responses = {}

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
    error_responses = {}

    def __call__(self) -> SimpleItemSchema:
        schema: DataPageSimpleItemSchema = super().__call__(None)
        if schema.data:
            return schema.data[0]
        else:
            raise ArtifactsHTTPStatusError(status_code=404, content=b"Item not found", json={})
