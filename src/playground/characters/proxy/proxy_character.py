from typing import Optional, Dict

from src.playground.characters import Character, FightResult, CharacterStats, CharacterQuest, \
    Inventory, Attack, Resistance, PercentDamage, EquipmentSlot, Level
from src.playground.characters.character import HarvestResult
from src.playground.characters.proxy.proxy_inventory import ProxyInventory
from src.playground.fabric.playground_world import PlaygroundWorld
from src.playground.items import Item, Items
from src.playground.items.crafting import EffectType
from src.playground.utilites.char_results import CharacterEstimator


class ProxyCharacter(Character):
    def __init__(self, level, equipment: Dict[EquipmentSlot, Items],
                 world: PlaygroundWorld):
        super().__init__("proxy")
        self._level = level
        self._world = world
        self._inventory = ProxyInventory(equipment=equipment)

    @property
    def inventory(self) -> Inventory:
        return self._inventory

    @property
    def character_quest(self) -> CharacterQuest:
        raise NotImplementedError

    @property
    def stats(self) -> CharacterStats:
        equipment = self.inventory.equipment
        hp = CharacterEstimator().estimate_hp(self._level)
        attack_earth = 0
        attack_water = 0
        attack_air = 0
        attack_fire = 0

        res_earth = 0
        res_water = 0
        res_air = 0
        res_fire = 0

        dmg_earth = 0
        dmg_water = 0
        dmg_air = 0
        dmg_fire = 0

        for slot, equip in equipment.items():

            item_details = self._world.item_details.get_item(equip.item)
            for effect in item_details.effects:
                match effect.type:
                    # Attack
                    case EffectType.ATTACK_FIRE:
                        attack_fire += effect.value
                    case EffectType.ATTACK_AIR:
                        attack_air += effect.value
                    case EffectType.ATTACK_WATER:
                        attack_water += effect.value
                    case EffectType.ATTACK_EARTH:
                        attack_earth += effect.value
                    # Resists
                    case EffectType.RESIST_FIRE:
                        res_fire += effect.value
                    case EffectType.RESIST_AIR:
                        res_air += effect.value
                    case EffectType.RESIST_WATER:
                        res_water += effect.value
                    case EffectType.RESIST_EARTH:
                        res_earth += effect.value
                    # Damage boost
                    case EffectType.DAMAGE_FIRE:
                        dmg_fire += effect.value
                    case EffectType.DAMAGE_AIR:
                        dmg_air += effect.value
                    case EffectType.DAMAGE_WATER:
                        dmg_water += effect.value
                    case EffectType.DAMAGE_EARTH:
                        dmg_earth += effect.value
                    # Others
                    case EffectType.HP:
                        hp += effect.value
        stats = CharacterStats(hp=hp,
                               level=Level(level=self._level, xp=0, max_xp=0),
                               attack=Attack(fire=attack_fire,
                                             air=attack_air,
                                             water=attack_water,
                                             earth=attack_earth),
                               resistance=Resistance(fire=res_fire,
                                                     air=res_air,
                                                     water=res_water,
                                                     earth=res_earth),
                               perc_damage=PercentDamage(fire=dmg_fire,
                                                         air=dmg_air,
                                                         water=dmg_water,
                                                         earth=dmg_earth),
                               # TOOO implement
                               skills=None,
                               gold=None,
                               haste=0,
                               speed=None)
        return stats

    def is_busy(self) -> bool:
        return False

    @property
    def position(self) -> tuple:
        raise NotImplementedError

    def move(self, x, y):
        raise NotImplementedError

    def fight(self) -> FightResult:
        raise NotImplementedError

    def harvest(self) -> HarvestResult:
        raise NotImplementedError

    def craft(self, recipe: Item, amount: int):
        raise NotImplementedError

    def recycle(self, item: Item, amount: int):
        raise NotImplementedError

    def deposit_item(self, item: Item, amount: int):
        raise NotImplementedError

    def deposit_gold(self, amount: int):
        raise NotImplementedError

    def withdraw_item(self, item: Item, amount: int):
        raise NotImplementedError

    def withdraw_gold(self, amount: int):
        raise NotImplementedError

    def grand_exchange_buy_item(self, item: Item, amount: int, price: int):
        raise NotImplementedError

    def grand_exchange_sell_item(self, item: Item, amount: int, price: int):
        raise NotImplementedError
