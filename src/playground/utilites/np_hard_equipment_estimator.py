import itertools
import logging
from typing import List, Dict

from src.playground.characters import Character, EquipmentSlot
from src.playground.characters.proxy.proxy_character import ProxyCharacter
from src.playground.constants import MAX_UTILITIES_EQUIPPED
from src.playground.errors import NotFoundException
from src.playground.fabric.playground_world import PlaygroundWorld
from src.playground.items import ItemType, Items, Item
from src.playground.items.crafting import ItemDetails
from src.playground.items.item import EffectType, ItemEffect
from src.playground.monsters import DetailedMonster
from src.playground.utilites.fight_results import FightEstimator

MAX_EQUIPMENT_COUNT = 5
logger = logging.getLogger(__name__)


class NPHardEquipmentEstimator:
    """
    NP Hard version of best equipment estimation
    """

    def __init__(self, world: PlaygroundWorld, available_equipment: List[ItemDetails], initial_equipment: Dict[EquipmentSlot, Items] = None,
                 use_utlities=True, winrate: float = 0.9, max_equipment_count=MAX_EQUIPMENT_COUNT):
        self.available_equipment = available_equipment
        self.use_utilities = use_utlities
        self.world = world
        self.winrate = winrate
        self.max_equipment_count = max_equipment_count
        self.initial_equipment = initial_equipment

    def optimal_vs_monster(self, character: Character, monster: DetailedMonster) -> Dict[EquipmentSlot, Items]:

        target_items_type = [ItemType.weapon, ItemType.helmet, ItemType.shield,
                             ItemType.body_armor,
                             ItemType.amulet, ItemType.leg_armor, ItemType.boots, ItemType.ring,
                             ItemType.artifact]
        if self.use_utilities:
            target_items_type.append(ItemType.utility)
        fighting_items = [item for item in self.available_equipment if
                          item.type in target_items_type]
        items_mapping = {item.code: item for item in fighting_items}
        slots_items: Dict[EquipmentSlot, List[Item]] = {}
        slot2type = {EquipmentSlot.WEAPON: ItemType.weapon,
                     EquipmentSlot.SHIELD: ItemType.shield,
                     EquipmentSlot.HELMET: ItemType.helmet,
                     EquipmentSlot.BODY_ARMOR: ItemType.body_armor,
                     EquipmentSlot.LEG_ARMOR: ItemType.leg_armor,
                     EquipmentSlot.BOOTS: ItemType.boots,
                     EquipmentSlot.RING1: ItemType.ring,
                     EquipmentSlot.RING2: ItemType.ring,
                     EquipmentSlot.AMULET: ItemType.amulet,
                     EquipmentSlot.ARTIFACT1: ItemType.artifact,
                     EquipmentSlot.ARTIFACT2: ItemType.artifact,
                     EquipmentSlot.ARTIFACT3: ItemType.artifact
                     }
        if self.use_utilities:
            slot2type.update({EquipmentSlot.UTILITY1: ItemType.utility,
                              EquipmentSlot.UTILITY2: ItemType.utility})
        for equipment_slot, item_type in slot2type.items():
            items_for_slot = [item for item in fighting_items if item.type == item_type]
            if items_for_slot:
                match equipment_slot:
                    case EquipmentSlot.WEAPON | EquipmentSlot.SHIELD | EquipmentSlot.HELMET | \
                    EquipmentSlot.BODY_ARMOR | EquipmentSlot.LEG_ARMOR | EquipmentSlot.BOOTS | \
                         EquipmentSlot.RING1 | EquipmentSlot.RING2 | EquipmentSlot.AMULET | \
                         EquipmentSlot.ARTIFACT1  |EquipmentSlot.ARTIFACT2 | \
                         EquipmentSlot.ARTIFACT3:
                        # Sorting by the best items
                        def sorting_key(item: ItemDetails) -> int:
                            return -item.level
                        max_level = max(items_for_slot, key=lambda item: item.level).level
                        items_with_max_level = len([item for item in items_for_slot if item.level==max_level])
                        # We don't need all items
                        count_items = max(self.max_equipment_count, items_with_max_level)
                        items_for_slot = sorted(items_for_slot, key=sorting_key)[:count_items]
                    case EquipmentSlot.UTILITY1 | EquipmentSlot.UTILITY2:
                        # Sorting by the worst items because it easy to find
                        def sorting_key(item: ItemDetails) -> int:
                            return item.level
                        items_for_slot = sorted(items_for_slot, key=sorting_key)
                        items_for_slot.append(None)
                    case _:
                        raise NotImplementedError

                slots_items[equipment_slot] = items_for_slot

        if self.initial_equipment is not None:
            for equipment_slot, items in self.initial_equipment.items():
                assert equipment_slot in slots_items
                slots_items[equipment_slot] = [items.item]


        item_slots = list(slots_items.keys())
        items = [slots_items[key] for key in item_slots]
        equips = itertools.product(*items)
        print("wait for solution")
        max_winrate = 0
        optimal_equipment = {}
        for equipment in equips:
            possible_optimal_equipment: Dict[EquipmentSlot, ItemDetails] = dict(zip(item_slots, equipment))
            for slot, equip in list(possible_optimal_equipment.items()):
                if equip is None:
                    del possible_optimal_equipment[slot]
            # Utilities processing
            # Continue if utilities are same
            utility1 = possible_optimal_equipment.get(EquipmentSlot.UTILITY1, None)
            utitlity2 = possible_optimal_equipment.get(EquipmentSlot.UTILITY2, None)
            if utility1 is not None and utitlity2 is not None:
                if utility1.code == utitlity2.code:
                    continue
                # If effects are same
                effects = [effect.type for
                            item in [utility1, utitlity2] for
                            effect in item.effects]
                if effects.count(EffectType.RESTORE_HP) > 1:
                    continue
                # If level different, only the same levels or last must be higher, to avoid repetition
                if utility1.level > utitlity2.level:
                    continue
            # Artifacts processing
            artifacts_set = set()
            artifacts_slots = [EquipmentSlot.ARTIFACT1, EquipmentSlot.ARTIFACT2,
                               EquipmentSlot.ARTIFACT3]
            for slot in artifacts_slots:
                if slot in possible_optimal_equipment:
                    artifacts_set.add(possible_optimal_equipment[slot].code)
                    del possible_optimal_equipment[slot]

            for artifact, slot in zip(artifacts_set, artifacts_slots):
                possible_optimal_equipment[slot] = items_mapping[artifact]
            #######################
            # Make it like equipment, converts to Items
            possible_items_equipment: Dict[EquipmentSlot, Items]= {}
            for slot, item in possible_optimal_equipment.items():
                if slot in [EquipmentSlot.UTILITY1, EquipmentSlot.UTILITY2]:
                    count = MAX_UTILITIES_EQUIPPED
                else:
                    count = 1
                possible_items_equipment[slot] = Items(item, count)

            proxy_character = ProxyCharacter(character.stats.level.level,
                                             possible_items_equipment,
                                             world=self.world)
            fight_estimator = FightEstimator(world=self.world)
            fight_result = fight_estimator.simulate_fights(proxy_character, monster)
            # Only for testing
            if fight_result.success_rate > max_winrate:
                max_winrate = fight_result.success_rate
                optimal_equipment = possible_items_equipment
                logger.info(f"New max winrate {max_winrate}")
                logger.info(f"New equipment {[item.item.code for item in possible_items_equipment.values()]}")
            if fight_result.success_rate >= self.winrate:
                return possible_items_equipment
        logger.warning(f"No solution found for monster {monster.name}")
        return optimal_equipment
