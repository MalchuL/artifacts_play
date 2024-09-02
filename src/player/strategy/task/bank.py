import threading
from typing import List, Optional

from src.player.players.player import Player
from src.player.strategy.character_strategy import CharacterStrategy
from src.player.strategy.utils.position import find_closest_position
from src.player.task import TaskInfo, items_to_player_task
from src.player.task_manager import WorldTaskManager, ManagerTask
from src.playground.fabric.playground_world import PlaygroundWorld
from src.playground.items import Items
from src.playground.utilites.map_finder import MapFinder, BuildingType
from tests.test_finders import world

_LOCK = threading.Lock()

class BankStrategy(CharacterStrategy):

    def __init__(self, player: Player, world: PlaygroundWorld,
                 deposit_items: List[Items] = None, deposit_gold=0,
                 withdraw_items: List[Items] = None, withdraw_gold=0):

        super().__init__(player=player, world=world)
        self.deposit_items = deposit_items
        self.deposit_gold = deposit_gold
        self.withdraw_items = withdraw_items
        self.withdraw_gold = withdraw_gold


    def deposit_withdraw_bank(self, deposit_items: List[Items] = None,
                              deposit_gold=0,
                              withdraw_items: List[Items] = None,
                              withdraw_gold=0) -> List[TaskInfo]:
        world = self.world
        map_finder = MapFinder(world)
        character = self.player.character
        bank_location = find_closest_position(character,
                                              map_finder.find_building(BuildingType.BANK))
        character.move(x=bank_location.x, y=bank_location.y)
        character.wait_until_ready()

        if deposit_items:
            for items in deposit_items:
                character.deposit_item(item=items.item, amount=items.quantity)
                character.wait_until_ready()
        if deposit_gold > 0:
            character.deposit_gold(amount=deposit_gold)
            character.wait_until_ready()
        if withdraw_items:
            # Check missed items and
            missed_items = []
            for required_items in withdraw_items:
                bank_items = world.bank.get_bank_item(required_items.item)
                if bank_items:
                    if required_items.quantity > bank_items.quantity:
                        missed_items.append(Items(item=required_items.item,
                                                  quantity=required_items.quantity - bank_items.quantity))
                else:
                    missed_items.append(required_items)
            if missed_items:
                out_task_infos = []
                for items in missed_items:
                    self.logger.info(f"Missed_items in bank={missed_items}, try to gather it")
                    out_task_infos.append(items_to_player_task(items, world=self.world))
                return out_task_infos
            # Withdraw items
            for items in withdraw_items:
                character.withdraw_item(item=items.item, amount=items.quantity)
                character.wait_until_ready()
        if withdraw_gold > 0:
            character.withdraw_gold(amount=withdraw_gold)
            character.wait_until_ready()

        self.logger.info(f"deposit_items={deposit_items}\n"
                         f"deposit_gold={deposit_gold}\n"
                         f"withdraw_items={withdraw_items}\n"
                         f"withdraw_gold={withdraw_gold}")
        return []

    def run(self)  -> List[TaskInfo]:
        with _LOCK:
            return self.deposit_withdraw_bank(deposit_items=self.deposit_items,
                                              deposit_gold=self.deposit_gold,
                                              withdraw_items=self.withdraw_items,
                                              withdraw_gold=self.withdraw_gold)
