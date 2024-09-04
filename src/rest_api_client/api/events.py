from src.rest_api_client.api.named_classes import PagedRequest
from src.rest_api_client.model import DataPageActiveEventSchema


class GetAllEvents(PagedRequest):
    """
    Get All Events
    Fetch events details.
    operationId: get_all_events_events_get
    """
    endpoint_pattern = '/events?page={page}&size={page_size}'
    method_name = 'get'
    response_schema = DataPageActiveEventSchema
    error_responses = {}

    def __call__(self) -> DataPageActiveEventSchema:
        return super().__call__(None)