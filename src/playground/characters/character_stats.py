from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Level:
    level: int
    xp: int
    max_xp: int


@dataclass(frozen=True)
class Attack:
    earth: int
    water: int
    fire: int
    air: int


@dataclass(frozen=True)
class Resistance:
    earth: int
    water: int
    fire: int
    air: int


@dataclass(frozen=True)
class PercentDamage:
    earth: int
    water: int
    fire: int
    air: int


@dataclass(frozen=True)
class SkillLevel:
    level: int
    xp: int
    max_xp: int


class SkillType(Enum):
    WOODCUTTING = "woodcutting"
    FISHING = "fishing"
    MINING = "mining"
    COOKING = "cooking"
    WEAPON_CRAFTING = "weaponcrafting"
    GEAR_CRAFTING = "gearcrafting"
    JEWERLY_CRAFTING = "jewelrycrafting"


@dataclass(frozen=True)
class Skills:
    woodcutting: SkillLevel
    mining: SkillLevel
    fishing: SkillLevel
    cooking: SkillLevel
    weaponcrafting: SkillLevel
    gearcrafting: SkillLevel
    jewelrycrafting: SkillLevel


@dataclass(frozen=True)
class Stats:
    hp: int
    attack: Attack
    resistance: Resistance

@dataclass(frozen=True)
class CharacterStats(Stats):
    gold: int
    speed: int
    haste: int
    level: Level
    skills: Skills
    perc_damage: PercentDamage
