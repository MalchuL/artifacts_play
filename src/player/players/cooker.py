import random
from typing import List

from src.player.players.base_player import BasePlayer
from src.player.players.player_types import PlayerType
from src.player.strategy.utils.items import merge_items, subtract_items
from src.player.task import TaskInfo, ResourcesTask, Resources, CraftingTask
from src.playground.characters import SkillType
from src.playground.items import Items
from src.playground.items.crafting import ItemDetails
from src.playground.utilites.items_finder import ItemFinder

FARM_COUNT = 10


class Cooker(BasePlayer):
    player_type = PlayerType.COOKER
    harvest_skills = [SkillType.FISHING]
    crafting_skills = [SkillType.COOKING]

    def _do_something(self) -> TaskInfo:
        # Try to cook already prepared resources
        items_in_bank = self._world.bank.get_bank_items()
        items_to_craft = self._world.item_details.get_crafts()
        items_can_to_be_cooked = [item for item in items_to_craft if
                                  item.craft.skill in self.crafting_skills and item.craft.level <= self.character.stats.skills.get_skill(
                                      item.craft.skill).level]
        available_items = merge_items(self.character.inventory.items, items_in_bank)
        available_items = subtract_items(available_items, self._world_tasks.reserved_items())
        available_items_mapping = {items.item.code: items for items in available_items}
        ready_to_cook: List[ItemDetails] = []
        for possible_item in items_can_to_be_cooked:
            recipe_mapping = {items.item.code: items for items in possible_item.craft.items}
            # Check if all items are presented in inventory or in bank
            is_all_items_ready_for_recipe = all(
                [(key in available_items_mapping) for key in recipe_mapping])
            if is_all_items_ready_for_recipe:
                if all([available_items_mapping[key].quantity >= recipe_mapping[key].quantity for
                        key in recipe_mapping]):
                    ready_to_cook.append(possible_item)

        if ready_to_cook:
            random_craft = random.choice(ready_to_cook)
            recipe_mapping = {items.item.code: items for items in random_craft.craft.items}
            count = min([available_items_mapping[key].quantity // recipe_mapping[key].quantity for key in
                         recipe_mapping]) * random_craft.craft.quantity
            easy_task = TaskInfo(
                crafting_task=CraftingTask(items=Items(random_craft, quantity=count)))
        else:
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
            easy_task = TaskInfo(resources_task=ResourcesTask(
                resources=Resources(resource=easy_resource, count=FARM_COUNT)))

        return easy_task

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
