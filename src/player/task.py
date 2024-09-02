from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

from src.playground.characters import SkillType, EquipmentSlot
from src.playground.fabric.playground_world import PlaygroundWorld
from src.playground.items import Items, Item
from src.playground.monsters import Monster
from src.playground.resources import Resource
from src.playground.utilites.items_finder import ItemFinder


@dataclass
class CraftingTask:
    skill_level: Optional[int] = None
    skill_type: Optional[SkillType] = None
    items: Optional[Items] = None

    def __repr__(self):
        if self.items:
            return f"CraftingTask({self.items.item.code}({self.items.quantity}))"
        else:
            return f"CraftingTask({self.skill_type}:{self.skill_level})"


@dataclass
class Resources:
    resource: Resource
    count: int


@dataclass
class ResourcesTask:
    skill_level: Optional[int] = None
    skill_type: Optional[SkillType] = None
    resources: Optional[Resources] = None
    items: Optional[Items] = None

    def __repr__(self):
        if self.resources:
            return f"ResourcesTask({self.resources.resource.code}({self.resources.count}))"
        elif self.items:
            return f"ResourcesTask({self.items.item.code}({self.items.quantity}))"
        else:
            return f"ResourcesTask({self.skill_type}:{self.skill_level})"


@dataclass
class Monsters:
    monster: Monster
    count: int


@dataclass
class MonsterTask:
    monsters: Optional[Monsters] = None
    items: Optional[Items] = None
    character_level: Optional[int] = None

    def __repr__(self):
        if self.monsters:
            return f"MonsterTask({self.monsters.monster.code}({self.monsters.count}))"
        elif self.items:
            return f"MonsterTask({self.items.item.code}({self.items.quantity}))"
        else:
            return f"MonsterTask(character_level:{self.character_level})"


@dataclass
class QuestTask:
    pass


@dataclass
class BankObject:
    items: Optional[List[Items]] = None
    gold: int = 0

    def __repr__(self):
        out_str = ""
        if self.items:
            out_str += f"Items:{self.items};"
        if self.gold:
            out_str += f"Gold:{self.gold};"
        return out_str


@dataclass
class BankTask:
    deposit: BankObject = field(default_factory=lambda: BankObject())
    withdraw: BankObject = field(default_factory=lambda: BankObject())
    deposit_all: bool = False

    def __repr__(self):
        out_str = ""
        if self.deposit.items:
            out_str += f"Deposit:{self.deposit};"
        if self.withdraw.items:
            out_str += f"Withdraw:{self.withdraw};"
        if self.deposit_all:
            out_str += f"Deposit all;"
        return f"BankTask({out_str})"


@dataclass
class EquipTask:
    items: Items
    slot: Optional[EquipmentSlot] = None

    def __repr__(self):
        return f"Equip task({self.items.item.code}({self.items.quantity}))"


@dataclass
class TaskInfo:
    crafting_task: Optional[CraftingTask] = None
    resources_task: Optional[ResourcesTask] = None
    monster_task: Optional[MonsterTask] = None
    quest_task: Optional[QuestTask] = None
    bank_task: Optional[BankTask] = None
    equip_task: Optional[EquipTask] = None

    def __repr__(self):
        out_str = ""
        if self.crafting_task:
            out_str += f"Crafting task: {self.crafting_task};"
        if self.resources_task:
            out_str += f"Resources task: {self.resources_task};"
        if self.monster_task:
            out_str += f"Monster task: {self.monster_task};"
        if self.quest_task:
            out_str += f"Quest task: {self.quest_task};"
        if self.bank_task:
            out_str += f"Bank task: {self.bank_task};"
        if self.equip_task:
            out_str += f"Equip task: {self.equip_task};"
        return f"TaskInfo({out_str})"


def items_to_player_task(items: Items, world: PlaygroundWorld) -> TaskInfo:
    finder = ItemFinder(world)
    if finder.find_item_in_monsters(items.item):
        return TaskInfo(monster_task=MonsterTask(items=items))
    if finder.find_item_in_resources(items.item):
        return TaskInfo(resources_task=ResourcesTask(items=items))
    if finder.find_item_in_crafts(items.item):
        return TaskInfo(crafting_task=CraftingTask(items=items))
    raise ValueError(f'Item {items.item} not found to create player task')
