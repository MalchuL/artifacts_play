from enum import Flag, auto


class PlayerType(Flag):
    BARBARIAN = auto()  # Who fights with monsters
    ADVENTURER = auto()  # Who done tasks
    HARVESTER = auto()  # Who harvests resources, mines
    COOKER = auto()  # Who cooks food and maybe harvest food
    CREATOR = auto()  # Who creates things