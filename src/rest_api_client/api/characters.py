from src.rest_api_client.api.named_classes import CharacterRequest
from src.rest_api_client.model import CharacterResponseSchema


class GetCharacter(CharacterRequest):
    """
    Get Character
    Retrieve the details of a character.
    operationId: get_character_characters__name__get
    """
    endpoint_pattern = '/characters/{name}'
    method_name = 'get'
    response_schema = CharacterResponseSchema
    error_responses = {404: 'Character not found.'}

    def __call__(self) -> CharacterResponseSchema:
        return super().__call__(None)
