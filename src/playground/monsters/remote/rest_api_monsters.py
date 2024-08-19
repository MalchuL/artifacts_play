import logging
from typing import Dict, List, Optional

from src.playground.characters.character_stats import Attack, Resistance
from src.playground.items.item import Item, DropItem
from src.playground.monsters.monster import DetailedMonster, Monster, MonsterStats
from src.playground.monsters.monster_manager import MonsterManager
from src.rest_api_client.api.items import GetAllItems
from src.rest_api_client.api.monsters import GetAllMonsters
from src.rest_api_client.client import AuthenticatedClient
from src.rest_api_client.model import MonsterSchema, DataPageMonsterSchema

logger = logging.getLogger(__name__)


class RestApiMonsterManager(MonsterManager):

    def __init__(self, client: AuthenticatedClient, pull_status=True):
        super().__init__()

        # Hidden variables
        self._client = client
        self._monsters: Optional[Dict[str, DetailedMonster]] = None
        if pull_status:
            self._monsters = self.__pull_state()

    @staticmethod
    def __parse_monster(state: MonsterSchema) -> DetailedMonster:
        return DetailedMonster(code=state.code,
                               name=state.name,
                               stats=MonsterStats(hp=state.hp,
                                                  level=state.level,
                                                  attack=Attack(earth=state.attack_earth,
                                                                water=state.attack_water,
                                                                fire=state.attack_fire,
                                                                air=state.attack_air),
                                                  resistance=Resistance(earth=state.res_earth,
                                                                        water=state.res_water,
                                                                        fire=state.res_fire,
                                                                        air=state.res_air)),
                               drops=[DropItem(item=Item(drop.code), rate=drop.rate,
                                               max_quantity=drop.max_quantity,
                                               min_quantity=drop.max_quantity) for drop in
                                      state.drops])

    def __pull_state(self) -> Dict[str, DetailedMonster]:
        date_page_monsters: DataPageMonsterSchema = GetAllMonsters(page=1, client=self._client)()
        total_pages = date_page_monsters.pages
        schemas: List[MonsterSchema] = list(date_page_monsters.data)

        for page in range(2, total_pages + 1):
            date_page_items: DataPageMonsterSchema = GetAllMonsters(page=page,
                                                                    client=self._client)()
            schemas.extend(date_page_items.data)

        monsters = {}
        for monster_schema in schemas:
            parsed_monster = self.__parse_monster(monster_schema)
            if parsed_monster.code in monsters:
                raise KeyError(
                    f"{parsed_monster.code}:{monsters[parsed_monster.code]}\n {parsed_monster} already defined"
                    f" for object. they are equal={monsters[parsed_monster.code] == parsed_monster}")
            monsters[parsed_monster.code] = parsed_monster

        return monsters

    @property
    def monsters(self) -> List[DetailedMonster]:
        return list(self._monsters.values())

    def get_monster_info(self, monster: Monster) -> DetailedMonster:
        return self._monsters[monster.code]
