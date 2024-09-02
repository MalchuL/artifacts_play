from src.player.strategy.player.can_complete.can_complete import CanComplete
from src.player.task import TaskInfo
from src.playground.fabric.playground_world import PlaygroundWorld
from src.playground.utilites.items_finder import ItemFinder


class CanCompleteResourceTask(CanComplete):

    def can_complete(self, task_info: TaskInfo):
        items_task = task_info.resources_task.items
        if items_task is not None:
            resources = ItemFinder(self.world).find_item_in_resources(items_task.item)
        elif task_info.resources_task.resources is not None:
            resources = [task_info.resources_task.resources.resource]
        else:
            raise ValueError(f"Task is not valid, got {task_info.resources_task}")
        for resource in resources:
            if resource.level <= self.player.character.stats.skills.get_skill(
                    resource.skill).level:
                return True
        return False
