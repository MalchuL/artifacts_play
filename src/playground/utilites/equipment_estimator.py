import random
from typing import List, Dict

import numpy as np
from numpy.linalg import matrix_rank
from qpsolvers import solve_qp, solve_ls

from src.playground.characters import Character, EquipmentSlot
from src.playground.items import ItemType
from src.playground.items.crafting import EffectType, ItemDetails, ItemEffect
from src.playground.monsters import DetailedMonster
from src.playground.utilites.char_results import CharacterEstimator

MAX_FIGHTS_LENGTH = 50

class EquipmentEstimator:
    def __init__(self, available_equipment: List[ItemDetails]):
        self.available_equipment = available_equipment

    def get_value_multiplier(self, effect: ItemEffect):
        if effect.type in [EffectType.DAMAGE_FIRE, EffectType.DAMAGE_AIR, EffectType.DAMAGE_WATER,
                           EffectType.DAMAGE_EARTH]:
            value = effect.value * 0.01  # Increased dealed damage. This only counts how much damage will be added
        elif effect.type in [EffectType.RESIST_FIRE, EffectType.RESIST_AIR,
                             EffectType.RESIST_WATER, EffectType.RESIST_EARTH]:
            value = 1 - effect.value * 0.01  # Damage reduction
        elif effect.type in [EffectType.ATTACK_FIRE, EffectType.ATTACK_AIR,
                             EffectType.ATTACK_WATER, EffectType.ATTACK_EARTH]:
            value = effect.value  # Same as damage
        else:
            value = 0
        return value

    def optimal_vs_monster(self, character: Character, monster: DetailedMonster):
        # Constraint - sum of damage >= hp
        # Constrain sum of enemy atacks < char hp
        # It's a task of quadratic programming

        target_items_type = [ItemType.weapon, ItemType.helmet, ItemType.shield,
                             ItemType.body_armor,
                             ItemType.amulet, ItemType.leg_armor, ItemType.boots, ItemType.ring,
                             ItemType.artifact]
        fighting_items = [item for item in self.available_equipment if
                          item.type in target_items_type]

        monster_hp = monster.stats.hp
        monster_resistance = monster.stats.resistance
        monster_attack = monster.stats.attack
        character_hp = CharacterEstimator().estimate_hp(character.stats.level.level)
        # Optimizing damage (and a little bit resistance), I'll use and quadratic optimization problem
        # Refer to https://pypi.org/project/qpsolvers/
        # P matrix is and attack + damage boost added to total if two items equipped together
        # q matrix is a damage and resist
        # G matrix is equipped each item type
        # h is restriction on item type that possible to equip
        # ub is maximal items that can be equipped several times
        # How much item damaged and resists
        item_vector = np.zeros(len(fighting_items))
        # additional_damage_matrix corresponds of added damage, only because it has different
        # formula this task has quadratic problem
        additional_damage_matrix = np.zeros((len(fighting_items), len(fighting_items)))
        #additional_damage_matrix += np.random.rand(*item_matrix.shape) * 0.005 / monster_hp
        for i, item1 in enumerate(fighting_items):
            for j, item2 in enumerate(fighting_items[i + 1:], start=i + 1):
                dealed_damage = 0
                # Calculate additional damage for each effect
                # We calculate only if attack and damage boost equipped together and adds ONLY damage boost
                for effect1 in item1.effects:
                    effect1_value = self.get_value_multiplier(effect1)
                    for effect2 in item2.effects:
                        effect2_value = self.get_value_multiplier(effect2)
                        effect = 0  # By default items not deals damage
                        effect_set = {effect1.type, effect2.type}
                        if effect_set == {EffectType.ATTACK_FIRE, EffectType.DAMAGE_FIRE}:
                            resistance_mult = (1 - monster_resistance.fire * 0.01)
                            effect = effect1_value * effect2_value * resistance_mult
                        elif effect_set == {EffectType.ATTACK_AIR, EffectType.DAMAGE_AIR}:
                            resistance_mult = (1 - monster_resistance.air * 0.01)
                            effect = effect1_value * effect2_value * resistance_mult
                        elif effect_set == {EffectType.ATTACK_WATER, EffectType.DAMAGE_WATER}:
                            resistance_mult = (1 - monster_resistance.water * 0.01)
                            effect = effect1_value * effect2_value * resistance_mult
                        elif effect_set == {EffectType.ATTACK_EARTH, EffectType.DAMAGE_EARTH}:
                            resistance_mult = (1 - monster_resistance.earth * 0.01)
                            effect = effect1_value * effect2_value * resistance_mult
                        # We calculate percent of monster hp dealt by single attack
                        dealed_damage += effect * 2 / monster_hp  # Because it divides by 2 in solver
                additional_damage_matrix[i, j] = dealed_damage
            # Calulate damage only for weapons
            item_effect = 0
            for effect1 in item1.effects:
                match effect1.type:
                    # Attack monster
                    case EffectType.ATTACK_FIRE:
                        item_effect += effect1.value * (1 - monster_resistance.fire * 0.01) / monster_hp
                    case EffectType.ATTACK_AIR:
                        item_effect += effect1.value * (1 - monster_resistance.air * 0.01) / monster_hp
                    case EffectType.ATTACK_WATER:
                        item_effect += effect1.value * (1 - monster_resistance.water * 0.01) / monster_hp
                    case EffectType.ATTACK_EARTH:
                        item_effect += effect1.value * (1 - monster_resistance.earth * 0.01) / monster_hp
                    # Character can longer fights
                    # Maximize resistance to monster attack
                    case EffectType.RESIST_FIRE:
                        item_effect += monster_attack.fire * effect1.value * 0.01 / character_hp / MAX_FIGHTS_LENGTH
                    case EffectType.RESIST_AIR:
                        item_effect += monster_attack.air * effect1.value * 0.01 / character_hp / MAX_FIGHTS_LENGTH
                    case EffectType.RESIST_WATER:
                        item_effect += monster_attack.water * effect1.value * 0.01 / character_hp / MAX_FIGHTS_LENGTH
                    case EffectType.RESIST_EARTH:
                        item_effect += monster_attack.earth * effect1.value * 0.01 / character_hp / MAX_FIGHTS_LENGTH
                    case EffectType.HP:
                        item_effect += effect1.value / character_hp / MAX_FIGHTS_LENGTH / 10  # 10 is hyperparameter
            item_vector[i] += item_effect
        additional_damage_matrix = np.maximum(additional_damage_matrix, additional_damage_matrix.transpose())  # Make it symmetrical
        #item_vector += np.random.rand(*item_vector.shape) * 0.005 / monster_hp

        # ----- Restricts -------
        # Currently I can't support HP restriction because we don't know number of steps ((
        # Restrict items in inventory
        less_conditions = []
        condition_matrix = []
        for i, item_type in enumerate(target_items_type):
            condition_vector = np.zeros(len(fighting_items))
            for j, item in enumerate(fighting_items):
                if item.type == item_type:
                    condition_vector[j] = 1
            less_condition = 1
            if item_type == ItemType.ring:
                less_condition = 2
            elif item_type == ItemType.artifact:
                less_condition = 3
            if sum(condition_vector) > 0.5:
                condition_matrix.append(condition_vector)
                less_conditions.append(less_condition)
        condition_matrix = np.stack(condition_matrix)
        less_conditions = np.array(less_conditions)
        #condition_matrix += np.random.rand(*condition_matrix.shape) * 0.005

        # ----- Upper bound -------
        upper_bound = np.ones_like(item_vector)
        for i, item in enumerate(fighting_items):
            if item.type == ItemType.ring:
                upper_bound[i] = 2
            # I don't sure that we can equip same artifacts several times
            # elif item.type == ItemType.artifact:
            #     upper_bound[i] = 3

        # Refer to https://pypi.org/project/qpsolvers/
        # Because we minimize values we multiply it by -1
        # Only single solver worked ((
        x = solve_qp(P=-additional_damage_matrix.astype(np.float64) * 1000,
                     q=-item_vector.astype(np.float64) * 1000,
                     G=condition_matrix.astype(np.float64),
                     h=less_conditions.astype(np.float64),
                     A=None,
                     b=None,
                     lb=np.zeros_like(item_vector).astype(np.float64),
                     ub=upper_bound.astype(np.float64),
                     solver="piqp")

        equipped_item: Dict[EquipmentSlot, ItemDetails] = {}
        for item_type in target_items_type:
            sorted_values = sorted(
                [(fighting_item, x[i]) for i, fighting_item in enumerate(fighting_items) if
                 fighting_item.type == item_type], key=lambda v: v[1], reverse=True)
            if item_type in [ItemType.weapon, ItemType.helmet, ItemType.shield,
                             ItemType.body_armor,
                             ItemType.amulet, ItemType.leg_armor, ItemType.boots]:
                # We find corresponding items
                if sorted_values:
                    slot = EquipmentSlot(item_type.value)
                    equipped_item[slot] = sorted_values[0][0]
            if item_type == ItemType.ring:
                for i, item in enumerate(sorted_values[:2]):
                    if item[1] > 1.5:  # Higher than threshold equip same ring 2 times
                        equipped_item[EquipmentSlot.RING1] = item[0]
                        equipped_item[EquipmentSlot.RING2] = item[0]
                        break
                    else:
                        slot = EquipmentSlot(ItemType.ring.value + str(i))
                        equipped_item[slot] = item[0]
        return equipped_item
