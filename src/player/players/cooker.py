import random

from src.player.players.base_player import BasePlayer
from src.player.players.player_types import PlayerType
from src.player.strategy.task.craft_item import CraftStrategy
from src.player.strategy.task.harvest_items import HarvestStrategy
from src.player.task import TaskInfo, ResourcesTask, Resources
from src.playground.characters import SkillType
from src.playground.utilites.items_finder import ItemFinder


FARM_COUNT = 100



class Cooker(BasePlayer):
    player_type = PlayerType.COOKER
    harvest_skills = [SkillType.FISHING]
    crafting_skills = [SkillType.COOKING]

    def _can_complete_task(self, task: TaskInfo):
        if super()._can_complete_task(task):
            return True
        # Is resource task, check resources and level of resources
        elif task.resources_task is not None:
            items_task = task.resources_task.items
            if items_task is not None:
                resources = ItemFinder(self._world).find_item_in_resources(items_task.item)
            elif task.resources_task.resources is not None:
                resources = [task.resources_task.resources.resource]
            else:
                raise ValueError(f"Task is not valid, got {task.resources_task}")
            for resource in resources:
                if resource.level <= self.character.stats.skills.get_skill(resource.skill).level:
                    return True
        elif task.crafting_task is not None:
            craft = ItemFinder(self._world).find_item_in_crafts(task.crafting_task.items.item)
            crafting_level = self.character.stats.skills.get_skill(craft.craft.skill).level
            if craft.craft.skill in self.crafting_skills and craft.craft.level <= crafting_level:
                return True
        else:
            raise ValueError("Task is not valid")

        return False

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

    def _task_to_actions(self, task: TaskInfo):
        if task.bank_task is not None:
            bank_task = task.bank_task
            return self._deposit_items(deposit_items=bank_task.deposit.items,
                                       deposit_gold=bank_task.deposit.gold,
                                       withdraw_items=bank_task.withdraw.items,
                                       withdraw_gold=bank_task.withdraw.gold,
                                       deposit_all=bank_task.deposit_all)
        elif task.equip_task is not None:
            equip_task = task.equip_task
            return self._equip_items(items=equip_task.items, slot=equip_task.slot)
        elif task.resources_task is not None:
            resource_task = task.resources_task
            strategy = HarvestStrategy(player=self, world=self._world,
                                       items=resource_task.items,
                                       resources=resource_task.resources,
                                       skill_type=resource_task.skill_level,
                                       farm_until_level=resource_task.skill_level)
            return strategy.run()
        elif task.crafting_task is not None:
            crafting_task = task.crafting_task
            strategy = CraftStrategy(player=self, world=self._world,
                                     items=crafting_task.items)
            return strategy.run()
        else:
            raise ValueError("Task is not valid")

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
