from typing import Union

from src.rest_api_client.api.named_classes import PagedRequest
from src.rest_api_client.client import Client, AuthenticatedClient
from src.rest_api_client.model import DataPageMapSchema, MapResponseSchema
from src.rest_api_client.requests.single_artifacts_request import SingleArtifactsRequest


class GetAllMaps(PagedRequest):
    """
    Get All Maps
    Fetch maps details.
    operationId: get_all_maps_maps__get
    """
    endpoint_pattern = '/maps/?page={page}&size={page_size}'
    method_name = 'get'
    response_schema = DataPageMapSchema
    error_responses = {404: 'Maps not found.'}

    def __call__(self) -> DataPageMapSchema:
        return super().__call__(None)


class GetMap(SingleArtifactsRequest):
    """
    Get Map
    Retrieve the details of a map.
    operationId: get_map_maps__x___y__get
    """
    endpoint_pattern = '/maps/{x}/{y}'
    method_name = 'get'
    response_schema = MapResponseSchema
    error_responses = {404: 'Map not found.'}

    def __init__(self, x: int, y: int, client: Union[Client, AuthenticatedClient]):
        super().__init__(x=x, y=y, client=client)

    def __call__(self) -> MapResponseSchema:
        return super().__call__(None)
