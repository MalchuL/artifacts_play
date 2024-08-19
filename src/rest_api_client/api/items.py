from src.rest_api_client.api.named_classes import PagedRequest, ObjectCodeRequest
from src.rest_api_client.model import DataPageItemSchema, ItemResponseSchema


class GetAllItems(PagedRequest):
    """
    Get All Items
    Fetch items details.
    operationId: get_all_items_items__get
    """
    endpoint_pattern = '/items/?page={page}&size={page_size}'
    method_name = 'get'
    response_schema = DataPageItemSchema
    error_responses = {404: 'Items not found.'}

    def __call__(self) -> DataPageItemSchema:
        return super().__call__(None)


class GetItem(ObjectCodeRequest):
    """
    Get Item
    Retrieve the details of a item.
    operationId: get_item_items__code__get
    """
    endpoint_pattern = '/items/{code}'
    method_name = 'get'
    response_schema = ItemResponseSchema
    error_responses = {404: 'Item not found.'}

    def __call__(self) -> ItemResponseSchema:
        return super().__call__(None)
