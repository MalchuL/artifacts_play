from src.player.players.base_player import BasePlayer
from src.player.players.player_types import PlayerType
from src.player.task import TaskInfo, ResourcesTask, Resources, MonsterTask, Monsters, \
    CraftingTask, NothingTask
from src.playground.characters.character_task import TaskType
from src.playground.items import Item, Items
from src.playground.monsters import Monster
from src.playground.utilites.map_finder import MapFinder, BuildingType


class Adventurer(BasePlayer):
    player_type = PlayerType.ADVENTURER

    def _do_something(self) -> TaskInfo:
        character = self.character
        quest = character.character_quest.get_current_task()
        if quest is None or character.character_quest.is_task_completed():
            character.wait_until_ready()
            location = MapFinder(self._world).find_building(BuildingType.TASKS_MANAGER)[0]
            character.move(location.x, location.y)
            character.wait_until_ready()
            if character.character_quest.is_task_completed():
                character.character_quest.complete_task()
            character.wait_until_ready()
            quest = character.character_quest.accept_new_task()
            character.wait_until_ready()

        match quest.task_type:
            case TaskType.RESOURCES:
                resource = self._world.resources.get_resource_info(quest.code)
                count = quest.total - quest.progress
                result_task = TaskInfo(resources_task=ResourcesTask(
                    resources=Resources(resource=resource, count=count)))
            case TaskType.MONSTERS:
                monster = Monster(quest.code)
                count = quest.total - quest.progress
                result_task = TaskInfo(monster_task=MonsterTask(
                    monsters=Monsters(monster=monster, count=count)))
            case TaskType.CRAFTS:
                item = Item(quest.code)
                count = quest.total - quest.progress
                result_task = TaskInfo(crafting_task=CraftingTask(
                    items=Items(item=item, quantity=count)))
            case _:
                raise ValueError(f"Unknown task type: {quest.task_type}")
        if self._can_complete_task(result_task):
            return result_task
        else:
            return TaskInfo(nothing_task=NothingTask())

    def _is_player_task(self, task: TaskInfo):
        quest = self.character.character_quest.get_current_task()
        if super()._is_player_task(task):
            return True
        elif task.resources_task is not None:
            resource_task = task.resources_task
            if resource_task.resources:
                code = resource_task.resources.resource.code
            else:
                return False
            return quest is not None and quest.task_type == TaskType.RESOURCES and quest.code == code
        elif task.crafting_task is not None:
            crafting_task = task.crafting_task
            if crafting_task.items:
                code = crafting_task.items.item.code
            else:
                return False
            return quest is not None and quest.task_type == TaskType.CRAFTS and quest.code == code
        elif task.monster_task is not None:
            monster_task = task.monster_task
            if monster_task.monsters:
                code = monster_task.monsters.monster.code
            else:
                return False
            return quest is not None and quest.task_type == TaskType.MONSTERS and quest.code == code
        else:
            return False
