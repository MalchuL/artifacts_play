from src.player.players.player import Player
from src.player.strategy.player.can_complete.can_complete import CanComplete
from src.player.task import TaskInfo
from src.playground.fabric.playground_world import PlaygroundWorld
from src.playground.monsters import Monster, DetailedMonster
from src.playground.utilites.fight_results import FightEstimator
from src.playground.utilites.items_finder import ItemFinder


class CanBeatMonster(CanComplete):
    def __init__(self, player: Player, world: PlaygroundWorld, success_rate: float = 0.99,
                 fight_number=100):
        super().__init__(player, world)
        self.success_rate = success_rate
        self.fight_number = fight_number

    def can_complete(self, task_info: TaskInfo):

        monster_task = task_info.monster_task
        if monster_task.monsters is not None:
            simple_monster: Monster = monster_task.monsters.monster
            monster: DetailedMonster = self.world.monsters.get_monster_info(simple_monster)
        elif monster_task.items is not None:
            finder = ItemFinder(world=self.world)
            monsters = finder.find_item_in_monsters(monster_task.items.item)
            monster: DetailedMonster = monsters[0]
        else:
            raise ValueError(f"No monster found, {monster_task}")
        simulator = FightEstimator(world=self.world, simulate_fights_number=self.fight_number)
        fight_result = simulator.simulate_fights(self.player.character, monster)
        return fight_result.success_rate > self.success_rate
