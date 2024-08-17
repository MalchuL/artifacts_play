from dataclasses import dataclass


@dataclass
class Level:
    level: int
    xp: int
    max_xp: int
    total_xp: int


@dataclass
class Attack:
    earth: int
    water: int
    fire: int
    air: int


@dataclass
class Resistance:
    earth: int
    water: int
    fire: int
    air: int


@dataclass
class PercentDamage:
    earth: int
    water: int
    fire: int
    air: int


@dataclass
class SkillLevel:
    level: int
    xp: int
    max_xp: int


@dataclass
class Skills:
    woodcutting: SkillLevel
    fishing: SkillLevel
    cooking: SkillLevel
    weapon_crafting: SkillLevel
    gear_crafting: SkillLevel
    jewelry_crafting: SkillLevel


@dataclass
class CharacterStats:
    hp: int
    gold: int
    speed: int
    haste: int
    char_level: Level
    skills: Skills
    attack: Attack
    resistance: Resistance
    perc_damage: PercentDamage
