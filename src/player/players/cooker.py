import random

from src.player.players.base_player import BasePlayer
from src.player.players.player_types import PlayerType
from src.player.task import TaskInfo, ResourcesTask, Resources
from src.playground.characters import SkillType
from src.playground.utilites.items_finder import ItemFinder


FARM_COUNT = 100



class Cooker(BasePlayer):
    player_type = PlayerType.COOKER
    harvest_skills = [SkillType.FISHING]
    crafting_skills = [SkillType.COOKING]


    def __find_easy_resources(self):
        resources = self._world.resources.resources
        filtered_resources = []
        for resource in resources:
            skill = resource.skill
            if skill not in self.harvest_skills:
                continue
            skill_level = resource.level
            if skill_level <= self.character.stats.skills.get_skill(skill).level:
                filtered_resources.append(resource)
        random_idx = random.randint(0, len(filtered_resources) - 1)
        easy_resource = filtered_resources[random_idx]
        return easy_resource

    def _do_something(self) -> TaskInfo:
        easy_resource = self.__find_easy_resources()
        task_info = TaskInfo(resources_task=ResourcesTask(
            resources=Resources(resource=easy_resource, count=FARM_COUNT)))
        return task_info


    def _is_player_task(self, task: TaskInfo):
        if super()._is_player_task(task):
            return True
        elif task.resources_task is not None:
            if task.resources_task.items is not None:
                finder = ItemFinder(self._world)
                resource = finder.find_item_in_resources(task.resources_task.items.item)[0]
            elif task.resources_task.resources is not None:
                resource = task.resources_task.resources.resource
            else:
                raise ValueError(f"Task is not valid, got {task.resources_task}")
            return resource.skill in self.harvest_skills
        elif task.crafting_task is not None:
            finder = ItemFinder(self._world)
            craft = finder.find_item_in_crafts(task.crafting_task.items.item)
            return craft is not None and craft.craft.skill in self.crafting_skills
        else:
            return False
