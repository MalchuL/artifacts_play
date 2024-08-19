from src.rest_api_client.api.named_classes import PagedRequest
from src.rest_api_client.model import MonsterResponseSchema, DataPageMonsterSchema
from src.rest_api_client.requests.single_artifacts_request import SingleArtifactsRequest


class GetAllMonsters(PagedRequest):
    """
    Get All Monsters
    Fetch monsters details.
    operationId: get_all_monsters_monsters__get
    """
    endpoint_pattern = '/monsters/?page={page}&size={page_size}'
    method_name = 'get'
    response_schema = DataPageMonsterSchema
    error_responses = {404: 'Monsters not found.'}

    def __call__(self) -> DataPageMonsterSchema:
        return super().__call__(None)


class GetMonster(SingleArtifactsRequest):
    """
    Get Monster
    Retrieve the details of a monster.
    operationId: get_monster_monsters__code__get
    """
    endpoint_pattern = '/monsters/{code}'
    method_name = 'get'
    response_schema = MonsterResponseSchema
    error_responses = {404: 'Monster not found.'}

    def __call__(self) -> MonsterResponseSchema:
        return super().__call__(None)
