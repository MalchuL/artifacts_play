from dataclasses import dataclass
from typing import Optional

from src.rest_api_client.client import AuthenticatedClient
from src.rest_api_client.model import CharacterSchema


@dataclass
class InternalCharacterMessage:
    """
    Internal state to message between Character and inner fields
    """
    client: AuthenticatedClient
    name: str
    char_schema: Optional[CharacterSchema] = None

