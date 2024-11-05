from typing import List

from src.player.strategy.player.can_complete.can_complete import CanComplete
from src.player.task import TaskInfo
from src.playground.characters import SkillType, Character
from src.playground.fabric.playground_world import PlaygroundWorld
from src.playground.utilites.items_finder import ItemFinder


class CanCompleteCraftingTask(CanComplete):
    def __init__(self, character: Character, world: PlaygroundWorld, crafting_skills: List[SkillType]):
        super().__init__(character, world)
        self.crafting_skills = crafting_skills

    def can_complete(self, task_info: TaskInfo):
        craft = ItemFinder(self.world).find_item_in_crafts(task_info.crafting_task.items.item)
        crafting_level = self.character.stats.skills.get_skill(craft.craft.skill).level
        if craft.craft.skill in self.crafting_skills and craft.craft.level <= crafting_level:
            return True
        return False
