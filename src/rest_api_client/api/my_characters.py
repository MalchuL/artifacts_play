from src.rest_api_client.api.named_classes import CharacterRequest
from ..model import SimpleItemSchema, GETransactionItemSchema, \
    CharacterFightResponseSchema, EquipSchema, DepositWithdrawGoldSchema, RecyclingResponseSchema, \
    TaskResponseSchema, RecyclingSchema, CraftingSchema, UnequipSchema, EquipmentResponseSchema, \
    SkillResponseSchema, GETransactionResponseSchema, \
    TaskRewardResponseSchema, DeleteItemResponseSchema, DestinationSchema, \
    CharacterMovementResponseSchema, BankItemTransactionResponseSchema, \
    BankGoldTransactionResponseSchema, BankExtensionTransactionResponseSchema, \
    TaskCancelledResponseSchema


class ActionMove(CharacterRequest):
    """
    Action Move
    Moves a character on the map using the map's X and Y position.
    operationId: action_move_my__name__action_move_post
    """
    endpoint_pattern = '/my/{name}/action/move'
    method_name = 'post'
    response_schema = CharacterMovementResponseSchema
    error_responses = {404: 'Map not found.',
                       486: 'An action is already in progress by your character.',
                       490: 'Character already at destination.',
                       498: 'Character not found.',
                       499: 'Character in cooldown.'}

    def __call__(self, data: DestinationSchema) -> CharacterMovementResponseSchema:
        return super().__call__(data)


class ActionEquipItem(CharacterRequest):
    """
    Action Equip Item
    Equip an item on your character.
    operationId: action_equip_item_my__name__action_equip_post
    """
    endpoint_pattern = '/my/{name}/action/equip'
    method_name = 'post'
    response_schema = EquipmentResponseSchema
    error_responses = {404: 'Item not found.',
                       478: 'Missing item or insufficient quantity.',
                       484: "Character can't equip more than 100 consumables in the same slot.",
                       485: 'This item is already equipped.',
                       486: 'An action is already in progress by your character.',
                       491: 'Slot is not empty.',
                       496: 'Character level is insufficient.',
                       498: 'Character not found.',
                       499: 'Character in cooldown.'}

    def __call__(self, data: EquipSchema) -> EquipmentResponseSchema:
        return super().__call__(data)


class ActionUnequipItem(CharacterRequest):
    """
    Action Unequip Item
    Unequip an item on your character.
    operationId: action_unequip_item_my__name__action_unequip_post
    """
    endpoint_pattern = '/my/{name}/action/unequip'
    method_name = 'post'
    response_schema = EquipmentResponseSchema
    error_responses = {404: 'Item not found.',
                       478: 'Missing item or insufficient quantity.',
                       486: 'An action is already in progress by your character.',
                       491: 'Slot is empty.',
                       497: 'Character inventory is full.',
                       498: 'Character not found.',
                       499: 'Character in cooldown.'}

    def __call__(self, data: UnequipSchema) -> EquipmentResponseSchema:
        return super().__call__(data)


class ActionFight(CharacterRequest):
    """
    Action Fight
    Start a fight against a monster on the character's map.
    operationId: action_fight_my__name__action_fight_post
    """
    endpoint_pattern = '/my/{name}/action/fight'
    method_name = 'post'
    response_schema = CharacterFightResponseSchema
    error_responses = {486: 'An action is already in progress by your character.',
                       497: 'Character inventory is full.',
                       498: 'Character not found.',
                       499: 'Character in cooldown.',
                       598: 'Monster not found on this map.'}

    def __call__(self) -> CharacterFightResponseSchema:
        return super().__call__(None)


class ActionGathering(CharacterRequest):
    """
    Action Gathering
    Harvest a resource on the character's map.
    operationId: action_gathering_my__name__action_gathering_post
    """
    endpoint_pattern = '/my/{name}/action/gathering'
    method_name = 'post'
    response_schema = SkillResponseSchema
    error_responses = {486: 'An action is already in progress by your character.',
                       493: 'Not skill level required.',
                       497: 'Character inventory is full.',
                       498: 'Character not found.',
                       499: 'Character in cooldown.',
                       598: 'Resource not found on this map.'}

    def __call__(self) -> SkillResponseSchema:
        return super().__call__(None)


class ActionCrafting(CharacterRequest):
    """
    Action Crafting
    Crafting an item. The character must be on a map with a workshop.
    operationId: action_crafting_my__name__action_crafting_post
    """
    endpoint_pattern = '/my/{name}/action/crafting'
    method_name = 'post'
    response_schema = SkillResponseSchema
    error_responses = {404: 'Craft not found.',
                       478: 'Missing item or insufficient quantity.',
                       486: 'An action is already in progress by your character.',
                       493: 'Not skill level required.',
                       497: 'Character inventory is full.',
                       498: 'Character not found.',
                       499: 'Character in cooldown.',
                       598: 'Workshop not found on this map.'}

    def __call__(self, data: CraftingSchema) -> SkillResponseSchema:
        return super().__call__(data)


class ActionDepositBank(CharacterRequest):
    """
    Action Deposit Bank
    Deposit an item in a bank on the character's map.
    operationId: action_deposit_bank_my__name__action_bank_deposit_post
    """
    endpoint_pattern = '/my/{name}/action/bank/deposit'
    method_name = 'post'
    response_schema = BankItemTransactionResponseSchema
    error_responses = {404: 'Item not found.',
                       461: 'A transaction is already in progress with this item/your golds in your bank.',
                       462: 'Your bank is full.',
                       478: 'Missing item or insufficient quantity.',
                       486: 'An action is already in progress by your character.',
                       498: 'Character not found.',
                       499: 'Character in cooldown.',
                       598: 'Bank not found on this map.'}

    def __call__(self, data: SimpleItemSchema) -> BankItemTransactionResponseSchema:
        return super().__call__(data)


class ActionDepositBankGold(CharacterRequest):
    """
    Action Deposit Bank Gold
    Deposit golds in a bank on the character's map.
    operationId: action_deposit_bank_gold_my__name__action_bank_deposit_gold_post
    """
    endpoint_pattern = '/my/{name}/action/bank/deposit/gold'
    method_name = 'post'
    response_schema = BankGoldTransactionResponseSchema
    error_responses = {461: 'A transaction is already in progress with this item/your golds in your bank.',
                       486: 'An action is already in progress by your character.',
                       492: 'Insufficient golds on your character.',
                       498: 'Character not found.',
                       499: 'Character in cooldown.',
                       598: 'Bank not found on this map.'}

    def __call__(self, data: DepositWithdrawGoldSchema) -> BankGoldTransactionResponseSchema:
        return super().__call__(data)


class ActionRecycling(CharacterRequest):
    """
    Action Recycling
    Recyling an item. The character must be on a map with a workshop (only for equipments and weapons).
    operationId: action_recycling_my__name__action_recycling_post
    """
    endpoint_pattern = '/my/{name}/action/recycling'
    method_name = 'post'
    response_schema = RecyclingResponseSchema
    error_responses = {404: 'Item not found.',
                       473: 'This item cannot be recycled.',
                       478: 'Missing item or insufficient quantity.',
                       486: 'An action is already in progress by your character.',
                       493: 'Not skill level required.',
                       497: 'Character inventory is full.',
                       498: 'Character not found.',
                       499: 'Character in cooldown.',
                       598: 'Workshop not found on this map.'}

    def __call__(self, data: RecyclingSchema) -> RecyclingResponseSchema:
        return super().__call__(data)


class ActionWithdrawBank(CharacterRequest):
    """
    Action Withdraw Bank
    Take an item from your bank and put it in the character's inventory.
    operationId: action_withdraw_bank_my__name__action_bank_withdraw_post
    """
    endpoint_pattern = '/my/{name}/action/bank/withdraw'
    method_name = 'post'
    response_schema = BankItemTransactionResponseSchema
    error_responses = {404: 'Item not found.',
                       461: 'A transaction is already in progress with this item/your golds in your bank.',
                       478: 'Missing item or insufficient quantity.',
                       486: 'An action is already in progress by your character.',
                       497: 'Character inventory is full.',
                       498: 'Character not found.',
                       499: 'Character in cooldown.',
                       598: 'Bank not found on this map.'}

    def __call__(self, data: SimpleItemSchema) -> BankItemTransactionResponseSchema:
        return super().__call__(data)


class ActionWithdrawBankGold(CharacterRequest):
    """
    Action Withdraw Bank Gold
    Withdraw gold from your bank.
    operationId: action_withdraw_bank_gold_my__name__action_bank_withdraw_gold_post
    """
    endpoint_pattern = '/my/{name}/action/bank/withdraw/gold'
    method_name = 'post'
    response_schema = BankGoldTransactionResponseSchema
    error_responses = {460: 'Insufficient golds in your bank.',
                       461: 'A transaction is already in progress with this item/your golds in your bank.',
                       486: 'An action is already in progress by your character.',
                       498: 'Character not found.',
                       499: 'Character in cooldown.',
                       598: 'Bank not found on this map.'}

    def __call__(self, data: DepositWithdrawGoldSchema) -> BankGoldTransactionResponseSchema:
        return super().__call__(data)


class ActionGeBuyItem(CharacterRequest):
    """
    Action Ge Buy Item
    Buy an item at the Grand Exchange on the character's map.
    operationId: action_ge_buy_item_my__name__action_ge_buy_post
    """
    endpoint_pattern = '/my/{name}/action/ge/buy'
    method_name = 'post'
    response_schema = GETransactionResponseSchema
    error_responses = {479: "You can't buy or sell that many items at the same time.",
                       480: 'No stock for this item.',
                       482: 'No item at this price.',
                       483: 'A transaction is already in progress on this item by a another character.',
                       486: 'An action is already in progress by your character.',
                       492: 'Insufficient golds on your character.',
                       497: 'Character inventory is full.',
                       498: 'Character not found.',
                       499: 'Character in cooldown.',
                       598: 'Grand Exchange not found on this map.'}

    def __call__(self, data: GETransactionItemSchema) -> GETransactionResponseSchema:
        return super().__call__(data)


class ActionGeSellItem(CharacterRequest):
    """
    Action Ge Sell Item
    Sell an item at the Grand Exchange on the character's map.
    operationId: action_ge_sell_item_my__name__action_ge_sell_post
    """
    endpoint_pattern = '/my/{name}/action/ge/sell'
    method_name = 'post'
    response_schema = GETransactionResponseSchema
    error_responses = {404: 'Item not found.',
                       478: 'Missing item or insufficient quantity.',
                       479: "You can't buy or sell that many items at the same time.",
                       482: 'No item at this price.',
                       483: 'A transaction is already in progress on this item by a another character.',
                       486: 'An action is already in progress by your character.',
                       498: 'Character not found.',
                       499: 'Character in cooldown.',
                       598: 'Grand Exchange not found on this map.'}

    def __call__(self, data: GETransactionItemSchema) -> GETransactionResponseSchema:
        return super().__call__(data)


class ActionBuyBankExpansion(CharacterRequest):
    """
    Action Buy Bank Expansion
    Buy a 20 slots bank expansion.
    operationId: action_buy_bank_expansion_my__name__action_bank_buy_expansion_post
    """
    endpoint_pattern = '/my/{name}/action/bank/buy_expansion'
    method_name = 'post'
    response_schema = BankExtensionTransactionResponseSchema
    error_responses = {486: 'An action is already in progress by your character.',
                       492: 'Insufficient golds on your character.',
                       498: 'Character not found.',
                       499: 'Character in cooldown.',
                       598: 'Bank not found on this map.'}

    def __call__(self) -> BankExtensionTransactionResponseSchema:
        return super().__call__(None)


class ActionAcceptNewTask(CharacterRequest):
    """
    Action Accept New Task
    Accepting a new task.
    operationId: action_accept_new_task_my__name__action_task_new_post
    """
    endpoint_pattern = '/my/{name}/action/task/new'
    method_name = 'post'
    response_schema = TaskResponseSchema
    error_responses = {486: 'An action is already in progress by your character.',
                       489: 'Character already has a task.',
                       498: 'Character not found.',
                       499: 'Character in cooldown.',
                       598: 'Tasks Master not found on this map.'}

    def __call__(self) -> TaskResponseSchema:
        return super().__call__(None)


class ActionCompleteTask(CharacterRequest):
    """
    Action Complete Task
    Complete a task.
    operationId: action_complete_task_my__name__action_task_complete_post
    """
    endpoint_pattern = '/my/{name}/action/task/complete'
    method_name = 'post'
    response_schema = TaskRewardResponseSchema
    error_responses = {486: 'An action is already in progress by your character.',
                       487: 'Character has no task.',
                       488: 'Character has not completed the task.',
                       497: 'Character inventory is full.',
                       498: 'Character not found.',
                       499: 'Character in cooldown.',
                       598: 'Tasks Master not found on this map.'}

    def __call__(self) -> TaskRewardResponseSchema:
        return super().__call__(None)


class ActionTaskExchange(CharacterRequest):
    """
    Action Task Exchange
    Exchange 3 tasks coins for a random reward. Rewards are exclusive resources for crafting  items.
    operationId: action_task_exchange_my__name__action_task_exchange_post
    """
    endpoint_pattern = '/my/{name}/action/task/exchange'
    method_name = 'post'
    response_schema = TaskRewardResponseSchema
    error_responses = {478: 'Missing item or insufficient quantity.',
                       486: 'An action is already in progress by your character.',
                       497: 'Character inventory is full.',
                       498: 'Character not found.',
                       499: 'Character in cooldown.',
                       598: 'Tasks Master not found on this map.'}

    def __call__(self) -> TaskRewardResponseSchema:
        return super().__call__(None)


class ActionTaskCancel(CharacterRequest):
    """
    Action Task Cancel
    Cancel a task for 1 tasks coin.
    operationId: action_task_cancel_my__name__action_task_cancel_post
    """
    endpoint_pattern = '/my/{name}/action/task/cancel'
    method_name = 'post'
    response_schema = TaskCancelledResponseSchema
    error_responses = {478: 'Missing item or insufficient quantity.',
                       486: 'An action is already in progress by your character.',
                       497: 'Character inventory is full.',
                       498: 'Character not found.',
                       499: 'Character in cooldown.',
                       598: 'Tasks Master not found on this map.'}

    def __call__(self) -> TaskCancelledResponseSchema:
        return super().__call__(None)


class ActionDeleteItem(CharacterRequest):
    """
    Action Delete Item
    Delete an item from your character's inventory.
    operationId: action_delete_item_my__name__action_delete_post
    """
    endpoint_pattern = '/my/{name}/action/delete'
    method_name = 'post'
    response_schema = DeleteItemResponseSchema
    error_responses = {478: 'Missing item or insufficient quantity.',
                       486: 'An action is already in progress by your character.',
                       498: 'Character not found.',
                       499: 'Character in cooldown.'}

    def __call__(self, data: SimpleItemSchema) -> DeleteItemResponseSchema:
        return super().__call__(data)
