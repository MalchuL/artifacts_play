import random
from src.player.players.harvester import Harvester
from src.player.players.player_types import PlayerType
from src.player.task import TaskInfo, ResourcesTask, Resources
from src.playground.characters import SkillType

FARM_COUNT = 20


class Creator(Harvester):
    player_type = PlayerType.CREATOR
    crafting_skills = [SkillType.WEAPON_CRAFTING, SkillType.JEWERLY_CRAFTING, SkillType.GEAR_CRAFTING]

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
