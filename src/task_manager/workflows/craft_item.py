import copy
from typing import Dict, List

from src.playground.characters import SkillType
from src.playground.items import Items, Item
from src.playground.utilites.map_finder import MapFinder, BuildingType
from .available_items import AvailableItems
from .character_task import CharacterTask
from .deposit_items import BankTask
from .task import Rerun


class CraftItemsTask(CharacterTask):
    def __init__(self, char_name: str, items: Items):
        super().__init__(char_name)
        self.items = items

    @staticmethod
    def available_items_task(char_name, required_items: List[Item]):
        task = AvailableItems(char_name=char_name,
                              required_items=required_items)
        task.start()
        output = task.outputs()
        return copy.deepcopy(output["available_items"])

    @staticmethod
    def gather_items_task(char_name, items: Items):
        from .gather_items_task import GatherItemsTask
        task = GatherItemsTask(char_name=char_name, items=items)
        task.start()

    @staticmethod
    def bank_items_task(char_name, items: List[Items]):
        task = BankTask(char_name=char_name, deposit_all_items=True, withdraw_items=items)
        task.start()

    def check_and_get_missed_items(self, char_name, crafting_items: Items):
        world = self.world

        item_schema = world.item_details.get_craft(crafting_items.item)

        # Find available items
        required_items: List[Items] = item_schema.craft.items
        available_items = self.available_items_task(char_name,
                                                    required_items=[items.item for items in
                                                                    required_items])
        available_items_dict: Dict[str, Items] = {items.item.code: items for items
                                                  in available_items}

        # We should keep in mind that single craft can produce several items
        required_multiplier = (crafting_items.quantity +
                               item_schema.craft.quantity - 1) // item_schema.craft.quantity
        # Check items that we missed

        missed_items = []
        for required_item in required_items:
            if required_item.item.code in available_items_dict:
                available_quantity = available_items_dict[required_item.item.code].quantity
            else:
                available_quantity = 0
            required_quantity = required_item.quantity * required_multiplier
            if available_quantity < required_quantity:
                missed_items.append(Items(item=required_item.item,
                                          quantity=required_quantity - available_quantity))

        if missed_items:
            self.logger.info(f"There are missed items {missed_items} to create {crafting_items}")
            from .gather_items_task import GatherItemsTask
            for items in missed_items:
                self.gather_items_task(char_name, items=items)
            raise Rerun("Rerun missed items")

    def craft_item(self, char_name, crafting_items: Items):
        self.logger.info(f"Try to create it={crafting_items}")
        self.check_and_get_missed_items(char_name, crafting_items)

        world = self.world
        crafted_items_amount = 0

        item_schema = world.item_details.get_craft(crafting_items.item)
        character = world.get_character(self.char_name)
        inventory_capacity = character.inventory.max_inventory_amount

        craft_schema = item_schema.craft
        # Character inventory size required for single craft
        required_inventory_size_to_craft = sum(item.quantity for item in craft_schema.items)
        # How many items we can craft per single call
        possible_craft_amount = inventory_capacity // required_inventory_size_to_craft * craft_schema.quantity

        crafting_steps = (crafting_items.quantity +
                          possible_craft_amount - 1) // possible_craft_amount
        self.logger.info(f"Number of steps to craft={crafting_steps}")
        for i in range(crafting_steps):
            if i == crafting_steps - 1:
                amount = crafting_items.quantity % possible_craft_amount
            else:
                amount = possible_craft_amount
            self.logger.info(f"Try to create target items={Items(crafting_items.item, amount)}")

            batch_items = [Items(item.item, item.quantity * amount)
                           for item in craft_schema.items]

            self.bank_items_task(char_name, batch_items)
            self.logger.info(f"Finding workshop")

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
            self.logger.info(f"Found workshop {workshop_location}")
            x, y = character.position
            if x != workshop_location.x or y != workshop_location.y:
                character.move(x=workshop_location.x, y=workshop_location.y)
            character.wait_until_ready()
            character.craft(recipe=crafting_items.item, amount=amount)
            character.wait_until_ready()
            crafted_items_amount += amount
            self.logger.info(
                f"Crafted items {crafting_items.item}={crafted_items_amount}/{crafting_items.quantity}")
        self.logger.info(f"Finish Required Items Search, crafted items:{crafting_items.quantity}")

    def run(self):
        return self.craft_item(self.char_name, crafting_items=self.items)
