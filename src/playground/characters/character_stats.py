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

    def get_skill(self, skill_type: SkillType) -> SkillLevel:
        match skill_type:
            case SkillType.WOODCUTTING:
                return self.woodcutting
            case SkillType.FISHING:
                return self.fishing
            case SkillType.MINING:
                return self.mining
            case SkillType.COOKING:
                return self.cooking
            case SkillType.WEAPON_CRAFTING:
                return self.weaponcrafting
            case SkillType.GEAR_CRAFTING:
                return self.gearcrafting
            case SkillType.JEWERLY_CRAFTING:
                return self.jewelrycrafting
            case _:
                raise ValueError(f"Unknown skill type {skill_type}")


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

