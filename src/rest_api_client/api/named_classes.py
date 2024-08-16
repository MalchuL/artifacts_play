from abc import ABC
from typing import Union

from src.rest_api_client.client import Client, AuthenticatedClient
from src.rest_api_client.requests.single_artifacts_request import SingleArtifactsRequest


class CharacterRequest(SingleArtifactsRequest, ABC):
    def __init__(self, name, client: Union[Client, AuthenticatedClient]):
        super().__init__(name=name, client=client)
