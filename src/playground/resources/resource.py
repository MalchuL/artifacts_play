from abc import abstractmethod
from dataclasses import dataclass
from typing import List

from src.playground.characters.character_stats import Stats, SkillType
from src.playground.items.item import Item, DropItem


@dataclass(frozen=True)
class Resource:
    code: str
    name: str
    skill: SkillType  # The skill required to gather this resource.
    level: int  # The skill level required to gather this resource.
    drops: List[DropItem]

    def __post_init__(self):
        assert self.skill in [SkillType.MINING, SkillType.WOODCUTTING, SkillType.FISHING,
                              SkillType.ALCHEMY], self.skill.value
