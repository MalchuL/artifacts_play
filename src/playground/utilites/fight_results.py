import copy
import math
import random
from dataclasses import dataclass, field
from typing import List, Dict

from src.playground.characters import Character, EquipmentSlot
from src.playground.characters.character import Result, FightResult
from src.playground.constants import MAX_FIGHTS_LENGTH, TURN_COOLDOWN
from src.playground.fabric.playground_world import PlaygroundWorld
from src.playground.items.item import EffectType
from src.playground.monsters import DetailedMonster

PERCENT_MULTIPLIER = 0.01


@dataclass
class FightResultsDetailed(FightResult):
    monster_hp: int = 0
    character_hp: int = 0
    spent_utilities: Dict[EquipmentSlot, int] = field(default_factory=dict)


@dataclass
class FightSimulationResult:
    success_rate: float
    result: FightResultsDetailed


class FightEstimator:

    def __init__(self, world: PlaygroundWorld, max_turns=MAX_FIGHTS_LENGTH, simulate_fights_number=30):
        self._max_turns = max_turns
        self._simulate_fights_number = simulate_fights_number
        self._world = world

    @staticmethod
    def _calculate_damage(attack, damage):
        return round(attack * (1 + damage * PERCENT_MULTIPLIER))

    @staticmethod
    def _calculate_resist(attack, resist):
        return round(attack * resist * PERCENT_MULTIPLIER)

    @staticmethod
    def _calculate_block(resist):
        block_chance = resist / 10 * PERCENT_MULTIPLIER
        return random.random() <= block_chance

    @staticmethod
    def _calculate_cooldown(turns, haste):
        return round(turns * 2 - (haste * PERCENT_MULTIPLIER) * (turns * 2))

    def simulate_fights(self, character: Character,
                        monster: DetailedMonster) -> FightSimulationResult:
        results: List[FightResultsDetailed] = []
        for i in range(self._simulate_fights_number):
            result = self.estimate_fight(character=character, monster=monster)
            results.append(result)
        win_rate = len([result for result in results if
                        result.result == Result.WIN]) / self._simulate_fights_number
        representative_fight = sorted(results, key=lambda result_: result_.cooldown)[self._simulate_fights_number // 2]
        return FightSimulationResult(success_rate=win_rate, result=representative_fight)

    def estimate_fight(self, character: Character, monster: DetailedMonster):
        logs = []
        character_stats = character.stats
        character_hp = character_stats.max_hp

        monster_stats = monster.stats
        monster_hp = monster_stats.max_hp
        utilities = copy.deepcopy(character.inventory.utilities_amount)
        utilities_count = {slot: 0 for slot, cons in utilities.items()}

        boost_dmg_fire = 0
        boost_dmg_water = 0
        boost_dmg_earth = 0
        boost_dmg_air = 0

        boost_res_fire = 0
        boost_res_water = 0
        boost_res_earth = 0
        boost_res_air = 0

        for slot, utility in character.inventory.utilities_amount.items():
            if utilities_count[slot] > utilities[slot].quantity:
                continue
            apply = False
            for effect in self._world.item_details.get_item(utility.item).effects:
                if effect.type == EffectType.BOOST_HP:
                    character_hp += effect.value
                    apply = True
                elif effect.type == EffectType.BOOST_DAMAGE_FIRE:
                    boost_dmg_fire += effect.value
                    apply = True
                elif effect.type == EffectType.BOOST_DAMAGE_AIR:
                    boost_dmg_air += effect.value
                    apply = True
                elif effect.type == EffectType.BOOST_DAMAGE_WATER:
                    boost_dmg_water += effect.value
                    apply = True
                elif effect.type == EffectType.BOOST_DAMAGE_EARTH:
                    boost_dmg_earth += effect.value
                    apply = True
                elif effect.type == EffectType.BOOST_RESIST_FIRE:
                    boost_res_fire += effect.value
                    apply = True
                elif effect.type == EffectType.BOOST_RESIST_AIR:
                    boost_res_air += effect.value
                    apply = True
                elif effect.type == EffectType.BOOST_RESIST_WATER:
                    boost_res_water += effect.value
                    apply = True
                elif effect.type == EffectType.BOOST_RESIST_EARTH:
                    boost_res_earth += effect.value
                    apply = True
            if apply:
                utilities_count[slot] += 1


        max_character_hp = character_hp

        i = 0
        for i in range(1, self._max_turns + 1):
            if i % 2 == 0:
                # Monster turn
                monster_attack_fire = self._calculate_damage(monster_stats.attack.fire, 0)
                monster_attack_water = self._calculate_damage(monster_stats.attack.water, 0)
                monster_attack_air = self._calculate_damage(monster_stats.attack.air, 0)
                monster_attack_earth = self._calculate_damage(monster_stats.attack.earth, 0)
                # Calculate resisted damage
                monster_attack_fire -= self._calculate_resist(monster_attack_fire,
                                                              character_stats.resistance.fire + boost_res_fire)
                monster_attack_water -= self._calculate_resist(monster_attack_water,
                                                               character_stats.resistance.water + boost_res_water)
                monster_attack_air -= self._calculate_resist(monster_attack_air,
                                                             character_stats.resistance.air + boost_res_air)
                monster_attack_earth -= self._calculate_resist(monster_attack_earth,
                                                               character_stats.resistance.earth + boost_res_earth)
                log_string = "Turn {turn}: The monster used {elemental} attack and dealt {damage} damage."
                # Calculate block probability
                fire_block = self._calculate_block(character_stats.resistance.fire + boost_res_fire)
                if not fire_block and monster_attack_fire > 0:
                    logs.append(log_string.format(turn=i, elemental="fire",
                                                  damage=monster_attack_fire))
                    character_hp -= monster_attack_fire
                water_block = self._calculate_block(character_stats.resistance.water + boost_res_water)
                if not water_block and monster_attack_water > 0:
                    logs.append(log_string.format(turn=i, elemental="water",
                                                  damage=monster_attack_water))
                    character_hp -= monster_attack_water
                air_block = self._calculate_block(character_stats.resistance.air + boost_res_air)
                if not air_block and monster_attack_air > 0:
                    logs.append(log_string.format(turn=i, elemental="air",
                                                  damage=monster_attack_air))
                    character_hp -= monster_attack_air
                earth_block = self._calculate_block(character_stats.resistance.earth + boost_res_earth)
                if not earth_block and monster_attack_earth > 0:
                    logs.append(log_string.format(turn=i, elemental="earth",
                                                  damage=monster_attack_earth))
                    character_hp -= monster_attack_earth

                if character_hp <= max_character_hp // 2:
                    for slot, utility in character.inventory.utilities_amount.items():
                        if utilities_count[slot] > utilities[slot].quantity:
                            continue
                        apply = False
                        for effect in self._world.item_details.get_item(utility.item).effects:
                            if effect.type == EffectType.RESTORE_HP:
                                character_hp += effect.value
                                apply = True
                        if apply:
                            utilities_count[slot] += 1

                if character_hp <= 0:
                    break
            else:
                # Character turn
                character_attack_fire = self._calculate_damage(character_stats.attack.fire,
                                                               character_stats.perc_damage.fire + boost_dmg_fire)
                character_attack_water = self._calculate_damage(character_stats.attack.water,
                                                                character_stats.perc_damage.water + boost_dmg_water)
                character_attack_air = self._calculate_damage(character_stats.attack.air,
                                                              character_stats.perc_damage.air + boost_dmg_air)
                character_attack_earth = self._calculate_damage(character_stats.attack.earth,
                                                                character_stats.perc_damage.earth + boost_dmg_earth)
                # Calculate resisted damage
                character_attack_fire -= self._calculate_resist(character_attack_fire,
                                                                monster_stats.resistance.fire)
                character_attack_water -= self._calculate_resist(character_attack_water,
                                                                 monster_stats.resistance.water)
                character_attack_air -= self._calculate_resist(character_attack_air,
                                                               monster_stats.resistance.air)
                character_attack_earth -= self._calculate_resist(character_attack_earth,
                                                                 monster_stats.resistance.earth)
                log_string = "Turn {turn}: The character used {elemental} attack and dealt {damage} damage."
                # Calculate block probability
                fire_block = self._calculate_block(monster_stats.resistance.fire)
                if not fire_block and character_attack_fire > 0:
                    logs.append(log_string.format(turn=i, elemental="fire",
                                                  damage=character_attack_fire))
                    monster_hp -= character_attack_fire
                water_block = self._calculate_block(monster_stats.resistance.water)
                if not water_block and character_attack_water > 0:
                    logs.append(log_string.format(turn=i, elemental="water",
                                                  damage=character_attack_water))
                    monster_hp -= character_attack_water
                air_block = self._calculate_block(monster_stats.resistance.air)
                if not air_block and character_attack_air > 0:
                    logs.append(log_string.format(turn=i, elemental="air",
                                                  damage=character_attack_air))
                    monster_hp -= character_attack_air
                earth_block = self._calculate_block(monster_stats.resistance.earth)
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
        cooldown = max(self._calculate_cooldown(turns, haste=character_stats.haste), TURN_COOLDOWN)
        fight_result = FightResultsDetailed(drops=[], result=result, turns=turns, gold=0, xp=0,
                                            logs=logs,
                                            cooldown=cooldown, monster_hp=monster_hp,
                                            character_hp=character_hp,
                                            spent_utilities=utilities_count)
        return fight_result
