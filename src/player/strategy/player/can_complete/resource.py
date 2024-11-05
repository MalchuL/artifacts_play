from src.player.strategy.player.can_complete.can_complete import CanComplete
from src.player.task import TaskInfo
from src.playground.utilites.items_finder import ItemFinder
from src.playground.utilites.map_finder import MapFinder


class CanCompleteResourceTask(CanComplete):

    def can_complete(self, task_info: TaskInfo):
        items_task = task_info.resources_task.items
        if items_task is not None:
            resources = ItemFinder(self.world).find_item_in_resources(items_task.item)
        elif task_info.resources_task.resources is not None:
            resources = [task_info.resources_task.resources.resource]
        else:
            raise ValueError(f"Task is not valid, got {task_info.resources_task}")
        map_finder = MapFinder(world=self.world)
        for resource in resources:
            if map_finder.find_resource(resource) and resource.level <= self.character.stats.skills.get_skill(resource.skill).level:
                return True
        return False
