import math
import random

from src.playground.characters import Character
from src.playground.characters.character import Result, FightResult
from src.playground.monsters import DetailedMonster

PERCENT_MULTIPLIER = 0.01
TURN_COOLDOWN = 5


class FightEstimator:

    def __init__(self, max_turns=50, simulate_fights_number=30):
        self._max_turns = max_turns
        self._simulate_fights_number = simulate_fights_number

    @staticmethod
    def calculate_damage(attack, damage):
        return round(attack * (1 + damage * PERCENT_MULTIPLIER))

    @staticmethod
    def calculate_resist(attack, resist):
        return round(attack * resist * PERCENT_MULTIPLIER)

    @staticmethod
    def calculate_block(resist):
        block_chance = resist / 10 * PERCENT_MULTIPLIER
        return random.random() <= block_chance

    @staticmethod
    def calculate_cooldown(turns, haste):
        return round(turns * 2 - (haste * PERCENT_MULTIPLIER) * (turns * 2))

    def estimate_fight(self, character: Character, monster: DetailedMonster):
        logs = []
        character_stats = character.stats
        character_hp = character_stats.hp
        monster_stats = monster.stats
        monster_hp = monster_stats.hp
        i = 0
        for i in range(1, self._max_turns + 1):
            if i % 2 == 0:
                # Monster turn
                monster_attack_fire = self.calculate_damage(monster_stats.attack.fire, 0)
                monster_attack_water = self.calculate_damage(monster_stats.attack.water, 0)
                monster_attack_air = self.calculate_damage(monster_stats.attack.air, 0)
                monster_attack_earth = self.calculate_damage(monster_stats.attack.earth, 0)
                # Calculate resisted damage
                monster_attack_fire -= self.calculate_resist(monster_attack_fire,
                                                             character_stats.resistance.fire)
                monster_attack_water -= self.calculate_resist(monster_attack_fire,
                                                              character_stats.resistance.water)
                monster_attack_air -= self.calculate_resist(monster_attack_fire,
                                                            character_stats.resistance.air)
                monster_attack_earth -= self.calculate_resist(monster_attack_fire,
                                                              character_stats.resistance.earth)
                log_string = "Turn {turn}: The monster used {elemental} attack and dealt {damage} damage."
                # Calculate block probability
                earth_block = self.calculate_block(character_stats.resistance.fire)
                if not earth_block and monster_attack_fire > 0:
                    logs.append(log_string.format(turn=i, elemental="fire",
                                                  damage=monster_attack_fire))
                    character_hp -= monster_attack_fire
                water_block = self.calculate_block(character_stats.resistance.water)
                if not water_block and monster_attack_water > 0:
                    logs.append(log_string.format(turn=i, elemental="water",
                                                  damage=monster_attack_water))
                    character_hp -= monster_attack_water
                air_block = self.calculate_block(character_stats.resistance.air)
                if not air_block and monster_attack_air > 0:
                    logs.append(log_string.format(turn=i, elemental="air",
                                                  damage=monster_attack_air))
                    character_hp -= monster_attack_air
                earth_block = self.calculate_block(character_stats.resistance.earth)
                if not earth_block and monster_attack_earth > 0:
                    logs.append(log_string.format(turn=i, elemental="earth",
                                                  damage=monster_attack_earth))
                    character_hp -= monster_attack_earth
                if character_hp <= 0:
                    break
            else:
                # Character turn
                character_attack_fire = self.calculate_damage(character_stats.attack.fire,
                                                              character_stats.perc_damage.fire)
                character_attack_water = self.calculate_damage(character_stats.attack.water,
                                                               character_stats.perc_damage.water)
                character_attack_air = self.calculate_damage(character_stats.attack.air,
                                                             character_stats.perc_damage.air)
                character_attack_earth = self.calculate_damage(character_stats.attack.earth,
                                                               character_stats.perc_damage.earth)
                # Calculate resisted damage
                character_attack_fire -= self.calculate_resist(character_attack_fire,
                                                               monster_stats.resistance.fire)
                character_attack_water -= self.calculate_resist(character_attack_fire,
                                                                monster_stats.resistance.water)
                character_attack_air -= self.calculate_resist(character_attack_fire,
                                                              monster_stats.resistance.air)
                character_attack_earth -= self.calculate_resist(character_attack_fire,
                                                                monster_stats.resistance.earth)
                log_string = "Turn {turn}: The character used {elemental} attack and dealt {damage} damage."
                # Calculate block probability
                fire_block = self.calculate_block(monster_stats.resistance.fire)
                if not fire_block and character_attack_fire > 0:
                    logs.append(log_string.format(turn=i, elemental="fire",
                                                  damage=character_attack_fire))
                    monster_hp -= character_attack_fire
                water_block = self.calculate_block(monster_stats.resistance.water)
                if not water_block and character_attack_water > 0:
                    logs.append(log_string.format(turn=i, elemental="water",
                                                  damage=character_attack_water))
                    monster_hp -= character_attack_water
                air_block = self.calculate_block(monster_stats.resistance.air)
                if not air_block and character_attack_air > 0:
                    logs.append(log_string.format(turn=i, elemental="air",
                                                  damage=character_attack_air))
                    monster_hp -= character_attack_air
                earth_block = self.calculate_block(monster_stats.resistance.earth)
                if not earth_block and character_attack_earth > 0:
                    logs.append(log_string.format(turn=i, elemental="earth",
                                                  damage=character_attack_earth))
                    monster_hp -= character_attack_earth
                if monster_hp <= 0:
                    break
        turns = i
        if turns < 50:
            if character_hp <= 0:
                result = Result.LOSE
            else:
                result = Result.WIN
        else:
            result = Result.DRAW
        cooldown = max(self.calculate_cooldown(turns, haste=character_stats.haste), TURN_COOLDOWN)
        fight_result = FightResult(drops=[], result=result, turns=turns, gold=0, xp=0, logs=logs,
                                   cooldown=cooldown)
        return fight_result