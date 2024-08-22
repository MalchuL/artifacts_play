from pprint import pprint

from dynaconf import settings

from src.playground.characters import Character, RestApiCharacter
from src.playground.monsters import MonsterManager, RestApiMonsterManager
from src.playground.utilites.char_results import CharacterEstimator
from src.playground.utilites.fight_results import FightEstimator
from src.rest_api_client.client import AuthenticatedClient


def test_fight_simulation():
    estimator = CharacterEstimator()
    assert estimator.estimate_hp(1) == 120
    assert estimator.estimate_hp(10) == 165
    assert estimator.estimate_hp(3) == 130
    assert estimator.estimate_hp(16) == 200

