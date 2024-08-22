from abc import abstractmethod, ABC
from typing import Union, Dict

from src.playground.bank import Bank, RestApiBank
from src.playground.characters import Character, RestApiCharacter
from src.playground.fabric.playground_world import PlaygroundWorld
from src.playground.items import ItemCraftingInfoManager, RestApiItemCraftingInfoManager
from src.playground.map import RestApiMapManager, MapManager
from src.playground.monsters import MonsterManager, RestApiMonsterManager
from src.playground.resources import ResourceManager, RestApiResourceManager
from src.rest_api_client.client import AuthenticatedClient, Client


# Fabric
class RestApiPlaygroundWorld(PlaygroundWorld):
    def __init__(self, client: Union[Client, AuthenticatedClient]):
        self._client = client

        self.__bank = None
        self.__crafting = None
        self.__map = None
        self.__monsters = None
        self.__resources = None
        self.__characters: Dict[str, Character] = {}

    @property
    def bank(self) -> Bank:
        if self.__bank is None:
            self.__bank = RestApiBank(self._client)
        return self.__bank

    @property
    def item_details(self) -> ItemCraftingInfoManager:
        if self.__crafting is None:
            self.__crafting = RestApiItemCraftingInfoManager(self._client)
        return self.__crafting

    @property
    def map(self) -> MapManager:
        if self.__map is None:
            self.__map = RestApiMapManager(self._client)
        return self.__map

    @property
    def monsters(self) -> MonsterManager:
        if self.__monsters is None:
            self.__monsters = RestApiMonsterManager(self._client)
        return self.__monsters

    @property
    def resources(self) -> ResourceManager:
        if self.__resources is None:
            self.__resources = RestApiResourceManager(self._client)
        return self.__resources

    def get_character(self, name: str) -> Character:
        if name not in self.__characters:
            self.__characters[name] = RestApiCharacter(name, self._client)
        return self.__characters[name]
