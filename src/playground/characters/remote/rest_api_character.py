import logging
import time
from datetime import datetime, timezone
from typing import Union, Optional

from attr import evolve
from dateutil.parser import parse as datetime_parser

from src.errors import CharacterInventoryFullException
from src.playground.character import Character
from src.playground.character_task import CharacterQuest
from src.playground.characters.remote.remote_inventory import RemoteInventory
from src.playground.characters.remote.remote_quest import RemoteCharacterQuest
from src.playground.crafting import CraftingRecipe
from src.playground.item import Item
from src.rest_api_client.api.characters import GetCharacter
from src.rest_api_client.api.my_characters import ActionMove, ActionFight, ActionGathering, \
    ActionDepositBank, ActionAcceptNewTask, ActionCrafting, ActionDepositBankGold, ActionRecycling, \
    ActionWithdrawBank, ActionWithdrawBankGold, ActionGeBuyItem, ActionGeSellItem, \
    ActionCompleteTask, ActionTaskExchange
from src.rest_api_client.client import AuthenticatedClient
from src.rest_api_client.model import CharacterSchema, CharacterMovementResponseSchema, \
    DestinationSchema, CharacterFightResponseSchema, SkillResponseSchema, SimpleItemSchema, \
    ActionItemBankResponseSchema, TaskResponseSchema, CraftingSchema, GoldResponseSchema, \
    DepositWithdrawGoldSchema, RecyclingSchema, RecyclingResponseSchema, \
    GETransactionResponseSchema, GETransactionItemSchema, TaskRewardResponseSchema

logger = logging.getLogger(__name__)


class RestApiCharacter(Character):
    def __init__(self, name, client: AuthenticatedClient):
        super().__init__(name)
        self._client = client

        # Hidden variables
        self.__state: Optional[CharacterSchema] = None
        self.__inventory: Optional[RemoteInventory] = None
        self.__char_quest: Optional[RemoteCharacterQuest] = None

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
            self._state = char_schema
        return self.__state

    @_state.setter
    def _state(self, state: CharacterSchema):
        assert isinstance(state, CharacterSchema)
        self.__state = state
        self.__state.cooldown_expiration = self.__convert_datetime(
            self.__state.cooldown_expiration)

    def __pull_state(self) -> CharacterSchema:
        with evolve(self._client) as client:
            char_schema: CharacterSchema = GetCharacter(self.name, client=client)().data
        return char_schema

    @property
    def inventory(self) -> RemoteInventory:
        if self.__inventory is None:
            self.__inventory = RemoteInventory(self)
        return self.__inventory

    @property
    def character_quest(self) -> RemoteCharacterQuest:
        if self.__char_quest is None:
            self.__char_quest = RemoteCharacterQuest(self)
        return self.__char_quest

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
        if (x, y) == tuple(self.position):
            return
        dest = DestinationSchema(x=x, y=y)
        move_call = ActionMove(name=self.name, client=self._client)
        result: CharacterMovementResponseSchema = move_call(dest)
        self._state = result.data.character
        logger.info("Move results " + str(result.data.destination))

    def fight(self):
        result: CharacterFightResponseSchema = ActionFight(name=self.name, client=self._client)()
        self._state = result.data.character
        logger.info("Fight results " + str(result.data.fight))

    def harvest(self):
        if self.inventory.is_inventory_full():
            raise CharacterInventoryFullException()
        result: SkillResponseSchema = ActionGathering(self.name, client=self._client)()
        self._state = result.data.character
        logger.info("Harvest results " + str(result.data.details))

    def craft(self, recipe: CraftingRecipe, amount: int):
        crafting_schema = CraftingSchema(code=recipe.item.code, quantity=amount)
        crafting_call = ActionCrafting(name=self.name, client=self._client)
        result: SkillResponseSchema = crafting_call(crafting_schema)
        self._state = result.data.character
        logger.info("Crafting results " + str(result.data.details))

    def deposit_item(self, item: Item, amount: int):
        simple_item_schema = SimpleItemSchema(code=item.code, quantity=amount)
        deposit_bank_call = ActionDepositBank(name=self.name, client=self._client)
        result: ActionItemBankResponseSchema = deposit_bank_call(simple_item_schema)
        self._state = result.data.character
        logger.info(f"Deposit items={simple_item_schema} into bank {result.data.bank}")

    def deposit_gold(self, amount: int):
        simple_gold_schema = DepositWithdrawGoldSchema(quantity=amount)
        deposit_bank_call = ActionDepositBankGold(name=self.name, client=self._client)
        result: GoldResponseSchema = deposit_bank_call(simple_gold_schema)
        self._state = result.data.character
        logger.info(f"Deposit gold={simple_gold_schema} into bank {result.data.bank}")

    def recycle(self, item: Item, amount: int):
        recycle_schema = RecyclingSchema(code=item.code, quantity=amount)
        recycle_call = ActionRecycling(name=self.name, client=self._client)
        result: RecyclingResponseSchema = recycle_call(recycle_schema)
        self._state = result.data.character
        logger.info(f"Recycle {item}, {result.data.details}")

    def withdraw_item(self, item: Item, amount: int):
        simple_item_schema = SimpleItemSchema(code=item.code, quantity=amount)
        withdraw_bank_call = ActionWithdrawBank(name=self.name, client=self._client)
        result: ActionItemBankResponseSchema = withdraw_bank_call(simple_item_schema)
        self._state = result.data.character
        logger.info(f"Withdraw items={simple_item_schema} from bank {result.data.item}")

    def withdraw_gold(self, amount: int):
        simple_gold_schema = DepositWithdrawGoldSchema(quantity=amount)
        withdraw_bank_call = ActionWithdrawBankGold(name=self.name, client=self._client)
        result: GoldResponseSchema = withdraw_bank_call(simple_gold_schema)
        self._state = result.data.character
        logger.info(f"Withdraw gold={simple_gold_schema} from bank {result.data.bank}")

    def grand_exchange_buy_item(self, item: Item, amount: int, price: int):
        transaction_schema = GETransactionItemSchema(code=item.code, quantity=amount, price=price)
        grand_exchange_buy_call = ActionGeBuyItem(name=self.name, client=self._client)
        result: GETransactionResponseSchema = grand_exchange_buy_call(transaction_schema)
        self._state = result.data.character
        logger.info(
            f"Buy items={transaction_schema} from Grand Exchange {result.data.transaction}")

    def grand_exchange_sell_item(self, item: Item, amount: int, price: int):
        transaction_schema = GETransactionItemSchema(code=item.code, quantity=amount, price=price)
        grand_exchange_sell_call = ActionGeSellItem(name=self.name, client=self._client)
        result: GETransactionResponseSchema = grand_exchange_sell_call(transaction_schema)
        self._state = result.data.character
        logger.info(
            f"Sell items={transaction_schema} from Grand Exchange {result.data.transaction}")

