import logging
import time
from datetime import datetime, timezone
from typing import Union, Optional

from attr import evolve
from dateutil.parser import parse as datetime_parser
from dynaconf import settings

from src.playground.character import Character, ItemSlot
from src.playground.crafting import CraftingRecipe
from src.playground.errors import CharacterInventoryFullException, ERRORS_MAPPING
from src.playground.inventory import Inventory
from src.playground.item import Item, Items
from src.playground.remote.openapi_client.artifacts_api_client import AuthenticatedClient
from src.playground.remote.openapi_client.artifacts_api_client.api.characters import \
    get_character_characters_name_get as get_character
from src.playground.remote.openapi_client.artifacts_api_client.api.my_characters import \
    action_move_my_name_action_move_post as move, \
    action_equip_item_my_name_action_equip_post as equip_item, \
    action_accept_new_task_my_name_action_task_new_post as accept_task, \
    action_fight_my_name_action_fight_post as fight, \
    action_gathering_my_name_action_gathering_post as gathering, \
    action_deposit_bank_my_name_action_bank_deposit_post as deposit_item
from src.playground.remote.openapi_client.artifacts_api_client.errors import UnexpectedStatus
from src.playground.remote.openapi_client.artifacts_api_client.models import DestinationSchema, \
    TaskResponseSchema, CharacterFightResponseSchema, SkillResponseSchema, CharacterSchema, \
    EquipmentResponseSchema, SimpleItemSchema, CharacterMovementResponseSchema, \
    ActionItemBankResponseSchema

logger = logging.getLogger(__name__)


class RestApiCharacter(Character):
    def __init__(self, name, client: AuthenticatedClient):
        super().__init__(name)
        self._client = client

        # Hidden variables
        self.__inventory: Optional[Inventory] = None
        self.__state: Optional[CharacterSchema] = None

    def _get_current_time(self):
        return self.__convert_datetime(datetime.now())

    @staticmethod
    def __convert_datetime(date_time: Union[str, datetime]):
        if isinstance(date_time, str):
            date_time = datetime_parser(date_time)
        return date_time.astimezone(timezone.utc)

    @property
    def _state(self):
        if self.__state is None:
            char_schema = self.__pull_state()
            self.__state = char_schema
        return self.__state

    @_state.setter
    def _state(self, state: CharacterSchema):
        self.__state = state
        self.__state.cooldown_expiration = self.__convert_datetime(
            self.__state.cooldown_expiration)

    def __pull_state(self) -> CharacterSchema:
        with evolve(self._client) as client:
            char_schema: CharacterSchema = get_character.sync(self.name, client=client).data
        return char_schema

    @property
    def inventory(self) -> Inventory:
        if self.__inventory is None:
            state = self._state
            self.__inventory = Inventory(capacity=len(state.inventory),
                                         max_inventory_size=state.inventory_max_items)
            for item_slot in state.inventory:
                if item_slot.quantity > 0:
                    new_item = Items(Item(code=item_slot.code), quantity=item_slot.quantity)
                    self.__inventory.add_item(new_item)
            logger.info(f"Instantiating character inventory: {self.__inventory}")
        # Update sizes
        self.__inventory.max_inventory_size = self._state.inventory_max_items
        return self.__inventory

    def __check_inventory(self):
        if settings.DEBUG_MODULES:
            schema_inventory = self._state.inventory
            inner_inventory = self.__inventory
            inner_inventory_items = inner_inventory.get_items()
            assert self._state.inventory_max_items == inner_inventory.max_inventory_size
            assert inner_inventory.capacity == len(schema_inventory)
            for schema_item in schema_inventory:
                if schema_item.quantity > 0 or schema_item.code:
                    assert inner_inventory_items[schema_item.code].quantity == schema_item.quantity

    def is_busy(self) -> bool:
        return self._state.cooldown_expiration >= self._get_current_time()

    def wait_until_ready(self):
        now = self._get_current_time()
        expiration = self._state.cooldown_expiration
        if expiration > now:
            diff_seconds = (expiration - now).total_seconds()
            time.sleep(diff_seconds)

    @property
    def position(self) -> tuple:
        return self._state.x, self._state.y

    def move(self, x, y):
        with evolve(self._client) as client:
            dest = DestinationSchema(x, y)
            result: CharacterMovementResponseSchema = move.sync(self.name, client=client, body=dest)
        self._state = result.data.character
        logger.info("Move results " + str(result.data.destination))

    def equip_item(self, item: Item, item_slot: ItemSlot):
        #result: EquipmentResponseSchema = equip_item.sync()
        raise NotImplementedError()

    def unequip_item(self, item_slot: ItemSlot):
        pass

    def fight(self):
        with evolve(self._client) as client:
            result: CharacterFightResponseSchema = fight.sync(self.name, client=client)
        self._state = result.data.character
        for new_item in result.data.fight.drops:
            self.inventory.add_item(Items(item=Item(new_item.code), quantity=new_item.quantity))
        self.__check_inventory()
        logger.info("Fight results " + str(result.data.fight))

    def harvest(self):
        if self.inventory.is_inventory_full():
            raise CharacterInventoryFullException()
        try:
            with evolve(self._client) as client:
                result: SkillResponseSchema = gathering.sync(self.name, client=client)
        except UnexpectedStatus as e:
            except_class = ERRORS_MAPPING[e.status_code]
            raise except_class() from e
        self._state = result.data.character
        for new_item in result.data.details.items:
            self.inventory.add_item(Items(item=Item(new_item.code), quantity=new_item.quantity))
        self.__check_inventory()
        logger.info("Harvest results " + str(result.data.details))

    def craft(self, recipe: CraftingRecipe, amount: int):
        pass

    def deposit_item(self, item: Item, amount: int) -> Items:
        self.inventory.take_items(item=item, amount=amount)
        with evolve(self._client) as client:
            simple_item_schema: SimpleItemSchema = SimpleItemSchema(code=item.code, quantity=amount)
            result: ActionItemBankResponseSchema = deposit_item.sync(self.name, body=simple_item_schema, client=client)
        self._state = result.data.character
        logger.info(f"Deposit items={simple_item_schema} into bank " + str(result.data.item))
        self.__check_inventory()
        return Items(item, amount)

    def deposit_gold(self, amount: int):
        pass

    def recycle(self, item: Item, amount: int):
        pass

    def withdraw_item(self, item: Item, amount: int):
        pass

    def withdraw_gold(self, amount: int):
        pass

    def grand_exchange_buy_item(self, item: Item, amount: int):
        pass

    def grand_exchange_sell_item(self, item: Item, amount: int):
        pass

    def accept_new_task(self):
        with evolve(self._client) as client:
            result: TaskResponseSchema = accept_task.sync(self.name, client=client)
        self._state = result.data.character

    def complete_task(self):
        pass

    def delete_item(self, item: Item):
        pass
