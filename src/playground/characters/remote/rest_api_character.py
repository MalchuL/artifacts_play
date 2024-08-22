import logging
import time
from datetime import datetime, timezone
from typing import Union

from dateutil.parser import parse as datetime_parser

from src.playground.errors import CharacterInventoryFullException
from src.playground.characters.character import Character, FightResult, Result, HarvestResult
from src.playground.characters.character_stats import CharacterStats, Level, Skills, SkillLevel, Attack, \
    Resistance, PercentDamage
from src.playground.characters.remote.errors import char_exception_handler
from src.playground.characters.remote.internal_message import InternalCharacterMessage
from src.playground.characters.remote.remote_inventory import RemoteInventory
from src.playground.characters.remote.remote_quest import RemoteCharacterQuest
from src.playground.items.item import Item, Items
from src.rest_api_client.api.characters import GetCharacter
from src.rest_api_client.api.my_characters import ActionMove, ActionFight, ActionGathering, \
    ActionDepositBank, ActionCrafting, ActionDepositBankGold, ActionRecycling, \
    ActionWithdrawBank, ActionWithdrawBankGold, ActionGeBuyItem, ActionGeSellItem
from src.rest_api_client.client import AuthenticatedClient
from src.rest_api_client.model import CharacterSchema, CharacterMovementResponseSchema, \
    DestinationSchema, CharacterFightResponseSchema, SkillResponseSchema, SimpleItemSchema, \
    ActionItemBankResponseSchema, CraftingSchema, GoldResponseSchema, \
    DepositWithdrawGoldSchema, RecyclingSchema, RecyclingResponseSchema, \
    GETransactionResponseSchema, GETransactionItemSchema, Result as ResultSchema

logger = logging.getLogger(__name__)


class RestApiCharacter(Character):
    def __init__(self, name, client: AuthenticatedClient, pull_status=True):
        super().__init__(name)
        self._client = client

        # Hidden variables
        state = None
        if pull_status:
            state = self.__pull_state()
        self.__state: InternalCharacterMessage = InternalCharacterMessage(name=self.name,
                                                                          client=client,
                                                                          char_schema=state)
        self.__inventory: RemoteInventory = RemoteInventory(self.__state)
        self.__char_quest: RemoteCharacterQuest = RemoteCharacterQuest(self.__state)

    def _get_current_time(self):
        return self.__convert_datetime(datetime.now())

    @staticmethod
    def __convert_datetime(date_time: Union[str, datetime]):
        if isinstance(date_time, str):
            date_time = datetime_parser(date_time)
        return date_time.astimezone(timezone.utc)

    @property
    def _state(self) -> CharacterSchema:
        if self.__state.char_schema is None:
            char_schema = self.__pull_state()
            self._state.state = char_schema
        return self.__state.char_schema

    @_state.setter
    def _state(self, state: CharacterSchema):
        assert isinstance(state, CharacterSchema)
        self.__state.char_schema = state
        self.__state.char_schema.cooldown_expiration = self.__convert_datetime(
            self.__state.char_schema.cooldown_expiration)

    def __pull_state(self) -> CharacterSchema:
        char_schema: CharacterSchema = GetCharacter(self.name, client=self._client)().data
        return char_schema

    @property
    def inventory(self) -> RemoteInventory:
        return self.__inventory

    @property
    def character_quest(self) -> RemoteCharacterQuest:
        return self.__char_quest

    @property
    def stats(self) -> CharacterStats:
        state = self._state
        return CharacterStats(hp=state.hp,
                              gold=state.gold,
                              speed=state.speed,
                              haste=state.haste,
                              level=Level(level=state.level,
                                          xp=state.xp,
                                          max_xp=state.max_xp,
                                          total_xp=state.total_xp),
                              attack=Attack(earth=state.attack_earth,
                                            water=state.attack_water,
                                            fire=state.attack_fire,
                                            air=state.attack_air),
                              resistance=Resistance(earth=state.res_earth,
                                                    water=state.res_water,
                                                    fire=state.res_fire,
                                                    air=state.res_air),
                              perc_damage=PercentDamage(earth=state.dmg_earth,
                                                        water=state.dmg_water,
                                                        fire=state.dmg_fire,
                                                        air=state.dmg_air),
                              skills=Skills(woodcutting=SkillLevel(level=state.woodcutting_level,
                                                                   xp=state.woodcutting_xp,
                                                                   max_xp=state.woodcutting_max_xp),
                                            mining=SkillLevel(level=state.mining_level,
                                                                   xp=state.mining_xp,
                                                                   max_xp=state.mining_max_xp),
                                            cooking=SkillLevel(level=state.cooking_level,
                                                               xp=state.cooking_xp,
                                                               max_xp=state.cooking_max_xp),
                                            fishing=SkillLevel(level=state.fishing_level,
                                                               xp=state.fishing_xp,
                                                               max_xp=state.fishing_max_xp),
                                            weaponcrafting=SkillLevel(
                                                level=state.weaponcrafting_level,
                                                xp=state.weaponcrafting_xp,
                                                max_xp=state.weaponcrafting_max_xp),
                                            gearcrafting=SkillLevel(
                                                level=state.gearcrafting_level,
                                                xp=state.gearcrafting_xp,
                                                max_xp=state.gearcrafting_max_xp),
                                            jewelrycrafting=SkillLevel(
                                                level=state.jewelrycrafting_level,
                                                xp=state.jewelrycrafting_xp,
                                                max_xp=state.jewelrycrafting_max_xp)))

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

    @char_exception_handler
    def move(self, x, y):
        if (x, y) == tuple(self.position):
            return
        dest = DestinationSchema(x=x, y=y)
        move_call = ActionMove(name=self.name, client=self._client)
        result: CharacterMovementResponseSchema = move_call(dest)
        self._state = result.data.character
        logger.debug("Move results " + str(result.data.destination))

    @char_exception_handler
    def fight(self) -> FightResult:
        result: CharacterFightResponseSchema = ActionFight(name=self.name, client=self._client)()
        self._state = result.data.character
        logger.debug(f"Fight results {str(result.data.fight)}")

        fight = result.data.fight
        result_fight = Result.WIN if fight.result == ResultSchema.win else Result.LOSE
        fight_result = FightResult(result=result_fight,
                                   drops=[Items(Item(item.code), item.quantity) for item in
                                          fight.drops],
                                   turns=fight.turns,
                                   xp=fight.xp,
                                   gold=fight.gold,
                                   cooldown=result.data.cooldown.total_seconds,
                                   logs=fight.logs)
        return fight_result

    @char_exception_handler
    def harvest(self) -> HarvestResult:
        if self.inventory.is_inventory_full():
            raise CharacterInventoryFullException()
        result: SkillResponseSchema = ActionGathering(self.name, client=self._client)()
        self._state = result.data.character
        logger.debug(f"Harvest results {str(result.data.details)}")
        harvest = result.data.details
        harvest_result = HarvestResult(drops=[Items(Item(item.code), item.quantity) for item in
                                              harvest.items],
                                       xp=harvest.xp)
        return harvest_result

    @char_exception_handler
    def craft(self, recipe: Item, amount: int):
        crafting_schema = CraftingSchema(code=recipe.code, quantity=amount)
        crafting_call = ActionCrafting(name=self.name, client=self._client)
        result: SkillResponseSchema = crafting_call(crafting_schema)
        self._state = result.data.character
        logger.debug("Crafting results " + str(result.data.details))

    @char_exception_handler
    def deposit_item(self, item: Item, amount: int):
        simple_item_schema = SimpleItemSchema(code=item.code, quantity=amount)
        deposit_bank_call = ActionDepositBank(name=self.name, client=self._client)
        result: ActionItemBankResponseSchema = deposit_bank_call(simple_item_schema)
        self._state = result.data.character
        logger.debug(f"Deposit items={simple_item_schema} into bank {result.data.bank}")

    @char_exception_handler
    def deposit_gold(self, amount: int):
        simple_gold_schema = DepositWithdrawGoldSchema(quantity=amount)
        deposit_bank_call = ActionDepositBankGold(name=self.name, client=self._client)
        result: GoldResponseSchema = deposit_bank_call(simple_gold_schema)
        self._state = result.data.character
        logger.debug(f"Deposit gold={simple_gold_schema} into bank {result.data.bank}")

    @char_exception_handler
    def recycle(self, item: Item, amount: int):
        recycle_schema = RecyclingSchema(code=item.code, quantity=amount)
        recycle_call = ActionRecycling(name=self.name, client=self._client)
        result: RecyclingResponseSchema = recycle_call(recycle_schema)
        self._state = result.data.character
        logger.debug(f"Recycle {item}, {result.data.details}")

    @char_exception_handler
    def withdraw_item(self, item: Item, amount: int):
        simple_item_schema = SimpleItemSchema(code=item.code, quantity=amount)
        withdraw_bank_call = ActionWithdrawBank(name=self.name, client=self._client)
        result: ActionItemBankResponseSchema = withdraw_bank_call(simple_item_schema)
        self._state = result.data.character
        logger.debug(f"Withdraw items={simple_item_schema} from bank {result.data.item}")

    @char_exception_handler
    def withdraw_gold(self, amount: int):
        simple_gold_schema = DepositWithdrawGoldSchema(quantity=amount)
        withdraw_bank_call = ActionWithdrawBankGold(name=self.name, client=self._client)
        result: GoldResponseSchema = withdraw_bank_call(simple_gold_schema)
        self._state = result.data.character
        logger.debug(f"Withdraw gold={simple_gold_schema} from bank {result.data.bank}")

    @char_exception_handler
    def grand_exchange_buy_item(self, item: Item, amount: int, price: int):
        transaction_schema = GETransactionItemSchema(code=item.code, quantity=amount, price=price)
        grand_exchange_buy_call = ActionGeBuyItem(name=self.name, client=self._client)
        result: GETransactionResponseSchema = grand_exchange_buy_call(transaction_schema)
        self._state = result.data.character
        logger.debug(
            f"Buy items={transaction_schema} from Grand Exchange {result.data.transaction}")

    @char_exception_handler
    def grand_exchange_sell_item(self, item: Item, amount: int, price: int):
        transaction_schema = GETransactionItemSchema(code=item.code, quantity=amount, price=price)
        grand_exchange_sell_call = ActionGeSellItem(name=self.name, client=self._client)
        result: GETransactionResponseSchema = grand_exchange_sell_call(transaction_schema)
        self._state = result.data.character
        logger.debug(
            f"Sell items={transaction_schema} from Grand Exchange {result.data.transaction}")
