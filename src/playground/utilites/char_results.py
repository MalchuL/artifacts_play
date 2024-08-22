import math
import random

from src.playground.characters import Character
from src.playground.characters.character import Result, FightResult
from src.playground.monsters import DetailedMonster

BASE_HP = 120


class CharacterEstimator:

    def __init__(self):
        pass

    def estimate_hp(self, level):
        return BASE_HP + 5 * (level - 1)
