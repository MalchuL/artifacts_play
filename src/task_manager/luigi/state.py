from dataclasses import dataclass

from src.playground.fabric.playground_world import PlaygroundWorld


@dataclass
class PlaygroundState:
    world: PlaygroundWorld


__state: PlaygroundState = None


def get_world():
    if __state is None:
        raise
    return __state.world


def set_world(world: PlaygroundWorld):
    global __state
    __state = PlaygroundState(world=world)
    return __state.world
