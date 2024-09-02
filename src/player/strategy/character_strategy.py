from abc import ABC

from src.player.players.player import Player
from src.player.strategy.strategy import Strategy
from src.playground.fabric.playground_world import PlaygroundWorld


class CharacterStrategy(ABC, Strategy):
    def __init__(self, player: Player, world: PlaygroundWorld):
        super().__init__(world, name=f"{player.player_id}:{self.__class__.__name__}")
        self.player = player
