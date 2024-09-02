from typing import List

from src.player.players.player import Player
from src.player.strategy.character_strategy import CharacterStrategy
from src.player.task import TaskInfo, BankTask, BankObject, CraftingTask
from src.playground.characters import SkillType
from src.playground.fabric.playground_world import PlaygroundWorld
from src.playground.items import Items
from src.playground.utilites.items_finder import ItemFinder
from src.playground.utilites.map_finder import MapFinder, BuildingType


class CraftStrategy(CharacterStrategy):
    def __init__(self, items: Items, player: Player, world: PlaygroundWorld):
        super().__init__(player, world)
        self.items = items

    def check_missed_items(self, required_items: List[Items]):
        items_finder = ItemFinder(self.world)
        missed_items = []
        for items in required_items:
            character_items = items_finder.find_item_on_character(self.player.character,
                                                                  items.item)
            if character_items:
                if character_items.quantity < items.quantity:
                    missed_items.append(Items(item=items.item,
                                              quantity=items.quantity - character_items.quantity))
                # Else we have enough items
            else:
                missed_items.append(items)
        return missed_items

    def get_reserved_count(self):
        reserved_count = 0
        for item in self.player.reserve_items:
            reserved_count += item.quantity
        return reserved_count

    def run(self) -> List[TaskInfo]:
        crafting_items = self.items
        character = self.player.character
        self.logger.info(f"Try to create {crafting_items}")

        world = self.world
        crafted_items_amount = 0

        item_schema = world.item_details.get_craft(crafting_items.item)
        inventory_capacity = character.inventory.max_inventory_amount - self.get_reserved_count()

        craft_schema = item_schema.craft
        # Character inventory size required for single craft
        required_inventory_size_to_craft = sum(item.quantity for item in craft_schema.items)
        # How many items we can craft per single call
        possible_craft_amount = inventory_capacity // required_inventory_size_to_craft * craft_schema.quantity

        crafting_steps = (crafting_items.quantity +
                          possible_craft_amount - 1) // possible_craft_amount
        self.logger.info(f"Number of steps to craft={crafting_steps}")
        amount = min(crafting_items.quantity, possible_craft_amount)

        batch_items: List[Items] = [Items(item.item, item.quantity * amount)
                                    for item in craft_schema.items]

        missed_items = self.check_missed_items(batch_items)

        if missed_items:
            out_tasks = [TaskInfo(crafting_task=CraftingTask(items=crafting_items)),
                         TaskInfo(bank_task=BankTask(withdraw=BankObject(items=batch_items),
                                                     deposit_all=True))
                         ]
            self.logger.info(f"Missed items {missed_items}. Try to find it in bank")
            return out_tasks

        skill2building = {SkillType.WEAPON_CRAFTING: BuildingType.WEAPON_CRAFTING_WORKSHOP,
                          SkillType.GEAR_CRAFTING: BuildingType.GEAR_CRAFTING_WORKSHOP,
                          SkillType.JEWERLY_CRAFTING: BuildingType.JEWERLY_CRAFTING_WORKSHOP,
                          SkillType.COOKING: BuildingType.COOKING,
                          SkillType.WOODCUTTING: BuildingType.WOODCUTTING,
                          SkillType.MINING: BuildingType.MINING,
                          }
        map_finder = MapFinder(world)
        building_type = skill2building[craft_schema.skill]
        workshop_location = map_finder.find_building(building_type=building_type)[0]
        self.logger.info(f"Found workshop {workshop_location} for crafting {craft_schema.skill}")
        x, y = character.position
        if x != workshop_location.x or y != workshop_location.y:
            character.move(x=workshop_location.x, y=workshop_location.y)
        character.wait_until_ready()
        character.craft(recipe=crafting_items.item, amount=amount)
        character.wait_until_ready()
        crafted_items_amount += amount
        self.logger.info(f"Crafted items {crafting_items.item}="
                         f"{crafted_items_amount}/{crafting_items.quantity}")

        if crafted_items_amount < crafting_items.quantity:
            out_tasks= [TaskInfo(crafting_task=CraftingTask(
                items=Items(crafting_items.item,
                            quantity=crafting_items.quantity - crafted_items_amount)))]
            return out_tasks
        else:
            return [TaskInfo(bank_task=BankTask(deposit_all=True))]
