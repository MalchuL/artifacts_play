from typing import List

import numpy as np
from numpy.linalg import matrix_rank
from qpsolvers import solve_qp

from src.playground.characters import Character
from src.playground.items import ItemType
from src.playground.items.crafting import EffectType, ItemDetails, ItemEffect
from src.playground.monsters import DetailedMonster


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
        id2effect = {i: effect_type for i, effect_type in enumerate(EffectType)}
        effect2id = {effect_type: i for i, effect_type in id2effect.items()}
        print(id2effect)
        print(effect2id)

        target_items_type = [ItemType.weapon, ItemType.helmet, ItemType.shield,
                             ItemType.body_armor,
                             ItemType.amulet, ItemType.leg_armor, ItemType.boots, ItemType.ring,
                             ItemType.artifact]
        fighting_items = [item for item in self.available_equipment if
                          item.type in target_items_type]

        monster_hp = monster.stats.hp
        monster_resistance = monster.stats.resistance
        # Optimizing damage
        # How much item damaged
        item_vector = np.zeros(len(fighting_items))
        # item_matrix corresponds of added damage
        item_matrix = np.zeros((len(fighting_items), len(fighting_items)))
        for i, item1 in enumerate(fighting_items):
            for j, item2 in enumerate(fighting_items[i + 1:], start=i + 1):
                dealed_damage = 0
                # Calculate damage for each effect
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

                        dealed_damage += effect * 2
                item_matrix[i, j] = dealed_damage
            # Calulate damage only for weapons
            item_effect = 0
            for effect1 in item1.effects:
                match effect1.type:
                    case EffectType.ATTACK_FIRE:
                        item_effect += effect1.value * (1 - monster_resistance.fire * 0.01)
                    case EffectType.ATTACK_AIR:
                        item_effect += effect1.value * (1 - monster_resistance.air * 0.01)
                    case EffectType.ATTACK_WATER:
                        item_effect += effect1.value * (1 - monster_resistance.water * 0.01)
                    case EffectType.ATTACK_EARTH:
                        item_effect += effect1.value * (1 - monster_resistance.earth * 0.01)

            item_vector[i] += item_effect
        item_matrix = np.maximum(item_matrix, item_matrix.transpose())  # Make it symmetrical
        print([item.code for item in fighting_items])
        print(item_matrix)
        print(item_vector)
        # ----- Restricts -------
        # Currently I can't support HP restriction because we don't know number of steps ((
        # Restrict items in inventory
        less_condition = np.ones(len(target_items_type))
        condition_matrix = np.zeros((len(target_items_type), len(fighting_items)))
        for i, item_type in enumerate(target_items_type):
            for j, item in enumerate(fighting_items):
                if item.type == item_type:
                    condition_matrix[i, j] = 1
            if item_type == ItemType.ring:
                less_condition[i] = 2
            elif item_type == ItemType.artifact:
                less_condition[i] = 3


        print(condition_matrix)
        print(less_condition)
        print(condition_matrix.shape, less_condition.shape)
        print(item_matrix.shape, item_vector.shape)
        print(matrix_rank(item_matrix), matrix_rank(condition_matrix))
        # Refer to https://pypi.org/project/qpsolvers/
        # Because we minimize values we multiply it by -1
        x = solve_qp(P=-item_matrix,
                     q=-item_vector,
                     G=condition_matrix,
                     h=less_condition,
                     A=None,
                     b=None,
                     lb=np.zeros_like(item_vector),
                     ub=np.ones_like(item_vector),
                     solver="clarabel")

        print(x)
        for i, item_type in enumerate(target_items_type):
            maximum = (None, 0)
            for j, item in enumerate(fighting_items):
                if item.type == item_type and x[j] > maximum[1]:
                    maximum = (item, x[j])
            print(maximum, item_type)
