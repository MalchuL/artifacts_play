from src.rest_api_client.api.named_classes import PagedRequest, ObjectCodeRequest
from src.rest_api_client.model import DataPageResourceSchema, ResourceResponseSchema


class GetAllResources(PagedRequest):
    """
    Get All Resources
    Fetch resources details.
    operationId: get_all_resources_resources__get
    """
    endpoint_pattern = '/resources/?page={page}&size={page_size}'
    method_name = 'get'
    response_schema = DataPageResourceSchema
    error_responses = {404: 'Resources not found.'}

    def __call__(self) -> DataPageResourceSchema:
        return super().__call__(None)


class GetResource(ObjectCodeRequest):
    """
    Get Resource
    Retrieve the details of a resource.
    operationId: get_resource_resources__code__get
    """
    endpoint_pattern = '/resources/{code}'
    method_name = 'get'
    response_schema = ResourceResponseSchema
    error_responses = {404: 'Ressource not found.'}

    def __call__(self) -> ResourceResponseSchema:
        return super().__call__(None)
