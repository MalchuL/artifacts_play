from src.player.players.harvester import Harvester
from src.player.players.player_types import PlayerType
from src.player.task import TaskInfo, NothingTask
from src.playground.characters import SkillType
from src.playground.utilites.items_finder import ItemFinder

FARM_COUNT = 20


class Creator(Harvester):
    player_type = PlayerType.CREATOR
    harvest_skills = []
    crafting_skills = [SkillType.WEAPON_CRAFTING, SkillType.JEWERLY_CRAFTING,
                       SkillType.GEAR_CRAFTING]

    def _do_something(self) -> TaskInfo:
        task_info = TaskInfo(nothing_task=NothingTask())
        return task_info

    def _is_player_task(self, task: TaskInfo):
        value = super()._is_player_task(task)
        if value and task.crafting_task is not None:
            finder = ItemFinder(self._world)
            craft = finder.find_item_in_crafts(task.crafting_task.items.item).craft
            if self.character.stats.skills.get_skill(craft.skill).level < craft.level:
                raise NotImplementedError(
                    f"Skill {craft.skill} is not enough to craft {craft}, Implement smth to upgrade skills automatically by character")
        return value