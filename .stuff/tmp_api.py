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


class ActionRest(CharacterRequest):
    """
    Action Rest
    Recovers hit points by resting. (1 second per 5 HP, minimum 3 seconds)
    operationId: action_rest_my__name__action_rest_post
    """
    endpoint_pattern = '/my/{name}/action/rest'
    method_name = 'post'
    response_schema = CharacterRestResponseSchema
    error_responses = {486: 'An action is already in progress by your character.',
                       498: 'Character not found.',
                       499: 'Character in cooldown.'}

    def __call__(self) -> CharacterRestResponseSchema:
        return super().__call__(None)


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
                       484: 'Character can't equip more than 100 utilitys in the same slot.',
                       485: 'This item is already equipped.',
                       486: 'An action is already in progress by your character.',
                       491: 'Slot is not empty.',
                       496: 'Character level is insufficient.',
                       497: 'Character inventory is full.',
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
                       483: 'Character has no enough HP to unequip this item.',
                       486: 'An action is already in progress by your character.',
                       491: 'Slot is empty.',
                       497: 'Character inventory is full.',
                       498: 'Character not found.',
                       499: 'Character in cooldown.'}

    def __call__(self, data: UnequipSchema) -> EquipmentResponseSchema:
        return super().__call__(data)


class ActionUseItem(CharacterRequest):
    """
    Action Use Item
    Use an item as a consumable.
    operationId: action_use_item_my__name__action_use_post
    """
    endpoint_pattern = '/my/{name}/action/use'
    method_name = 'post'
    response_schema = UseItemResponseSchema
    error_responses = {404: 'Item not found.',
                       476: 'This item is not a consumable.',
                       478: 'Missing item or insufficient quantity.',
                       486: 'An action is already in progress by your character.',
                       496: 'Character level is insufficient.',
                       498: 'Character not found.',
                       499: 'Character in cooldown.'}

    def __call__(self, data: SimpleItemSchema) -> UseItemResponseSchema:
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


class ActionDepositBankGold(CharacterRequest):
    """
    Action Deposit Bank Gold
    Deposit gold in a bank on the character's map.
    operationId: action_deposit_bank_gold_my__name__action_bank_deposit_gold_post
    """
    endpoint_pattern = '/my/{name}/action/bank/deposit/gold'
    method_name = 'post'
    response_schema = BankGoldTransactionResponseSchema
    error_responses = {461: 'A transaction is already in progress with this item/your gold in your bank.',
                       486: 'An action is already in progress by your character.',
                       492: 'Insufficient gold on your character.',
                       498: 'Character not found.',
                       499: 'Character in cooldown.',
                       598: 'Bank not found on this map.'}

    def __call__(self, data: DepositWithdrawGoldSchema) -> BankGoldTransactionResponseSchema:
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
                       461: 'A transaction is already in progress with this item/your gold in your bank.',
                       462: 'Your bank is full.',
                       478: 'Missing item or insufficient quantity.',
                       486: 'An action is already in progress by your character.',
                       498: 'Character not found.',
                       499: 'Character in cooldown.',
                       598: 'Bank not found on this map.'}

    def __call__(self, data: SimpleItemSchema) -> BankItemTransactionResponseSchema:
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
                       461: 'A transaction is already in progress with this item/your gold in your bank.',
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
    error_responses = {460: 'Insufficient gold in your bank.',
                       461: 'A transaction is already in progress with this item/your gold in your bank.',
                       486: 'An action is already in progress by your character.',
                       498: 'Character not found.',
                       499: 'Character in cooldown.',
                       598: 'Bank not found on this map.'}

    def __call__(self, data: DepositWithdrawGoldSchema) -> BankGoldTransactionResponseSchema:
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
                       492: 'Insufficient gold on your character.',
                       498: 'Character not found.',
                       499: 'Character in cooldown.',
                       598: 'Bank not found on this map.'}

    def __call__(self) -> BankExtensionTransactionResponseSchema:
        return super().__call__(None)


class ActionRecycling(CharacterRequest):
    """
    Action Recycling
    Recycling an item. The character must be on a map with a workshop (only for equipments and weapons).
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


class ActionGeBuyItem(CharacterRequest):
    """
    Action Ge Buy Item
    Buy an item at the Grand Exchange on the character's map.
    operationId: action_ge_buy_item_my__name__action_grandexchange_buy_post
    """
    endpoint_pattern = '/my/{name}/action/grandexchange/buy'
    method_name = 'post'
    response_schema = GETransactionResponseSchema
    error_responses = {404: 'Order not found.',
                       434: 'This offer does not contain as many items.',
                       435: 'You can't buy to yourself.',
                       436: 'A transaction is already in progress on this order by a another character.',
                       486: 'An action is already in progress by your character.',
                       492: 'Insufficient gold on your character.',
                       497: 'Character inventory is full.',
                       498: 'Character not found.',
                       499: 'Character in cooldown.',
                       598: 'Grand Exchange not found on this map.'}

    def __call__(self, data: GEBuyOrderSchema) -> GETransactionResponseSchema:
        return super().__call__(data)


class ActionGeCreateSellOrder(CharacterRequest):
    """
    Action Ge Create Sell Order
    Create a sell order at the Grand Exchange on the character's map. Please note that a 5% sales tax is charged.
    operationId: action_ge_create_sell_order_my__name__action_grandexchange_sell_post
    """
    endpoint_pattern = '/my/{name}/action/grandexchange/sell'
    method_name = 'post'
    response_schema = GECreateOrderTransactionResponseSchema
    error_responses = {404: 'Item not found.',
                       433: 'You can't create more than 100 orders at the same time.',
                       437: 'This item cannot be sold.',
                       478: 'Missing item or insufficient quantity.',
                       486: 'An action is already in progress by your character.',
                       492: 'Insufficient gold on your character.',
                       498: 'Character not found.',
                       499: 'Character in cooldown.',
                       598: 'Grand Exchange not found on this map.'}

    def __call__(self, data: GEOrderCreationrSchema) -> GECreateOrderTransactionResponseSchema:
        return super().__call__(data)


class ActionGeCancelSellOrder(CharacterRequest):
    """
    Action Ge Cancel Sell Order
    Cancel a sell order at the Grand Exchange on the character's map.
    operationId: action_ge_cancel_sell_order_my__name__action_grandexchange_cancel_post
    """
    endpoint_pattern = '/my/{name}/action/grandexchange/cancel'
    method_name = 'post'
    response_schema = GETransactionResponseSchema
    error_responses = {404: 'Order not found.',
                       436: 'A transaction is already in progress on this order by a another character.',
                       438: 'You can't cancel an order that is not yours.',
                       486: 'An action is already in progress by your character.',
                       497: 'Character inventory is full.',
                       498: 'Character not found.',
                       499: 'Character in cooldown.',
                       598: 'Grand Exchange not found on this map.'}

    def __call__(self, data: GECancelOrderSchema) -> GETransactionResponseSchema:
        return super().__call__(data)


class ActionCompleteTask(CharacterRequest):
    """
    Action Complete Task
    Complete a task.
    operationId: action_complete_task_my__name__action_task_complete_post
    """
    endpoint_pattern = '/my/{name}/action/task/complete'
    method_name = 'post'
    response_schema = TasksRewardDataResponseSchema
    error_responses = {486: 'An action is already in progress by your character.',
                       487: 'Character has no task.',
                       488: 'Character has not completed the task.',
                       497: 'Character inventory is full.',
                       498: 'Character not found.',
                       499: 'Character in cooldown.',
                       598: 'Tasks Master not found on this map.'}

    def __call__(self) -> TasksRewardDataResponseSchema:
        return super().__call__(None)


class ActionTaskExchange(CharacterRequest):
    """
    Action Task Exchange
    Exchange 6 tasks coins for a random reward. Rewards are exclusive items or resources.
    operationId: action_task_exchange_my__name__action_task_exchange_post
    """
    endpoint_pattern = '/my/{name}/action/task/exchange'
    method_name = 'post'
    response_schema = TasksRewardDataResponseSchema
    error_responses = {478: 'Missing item or insufficient quantity.',
                       486: 'An action is already in progress by your character.',
                       497: 'Character inventory is full.',
                       498: 'Character not found.',
                       499: 'Character in cooldown.',
                       598: 'Tasks Master not found on this map.'}

    def __call__(self) -> TasksRewardDataResponseSchema:
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


class ActionTaskTrade(CharacterRequest):
    """
    Action Task Trade
    Trading items with a Tasks Master.
    operationId: action_task_trade_my__name__action_task_trade_post
    """
    endpoint_pattern = '/my/{name}/action/task/trade'
    method_name = 'post'
    response_schema = TaskTradeResponseSchema
    error_responses = {474: 'Character does not have this task.',
                       475: 'Character have already completed the task or are trying to trade too many items.',
                       478: 'Missing item or insufficient quantity.',
                       486: 'An action is already in progress by your character.',
                       498: 'Character not found.',
                       499: 'Character in cooldown.',
                       598: 'Tasks Master not found on this map.'}

    def __call__(self, data: SimpleItemSchema) -> TaskTradeResponseSchema:
        return super().__call__(data)


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


class GetAllCharactersLogs(SingleArtifactsRequest):
    """
    Get All Characters Logs
    History of the last 100 actions of all your characters.
    operationId: get_all_characters_logs_my_logs_get
    """
    endpoint_pattern = '/my/logs'
    method_name = 'get'
    response_schema = DataPageLogSchema
    error_responses = {404: 'Logs not found.',
                       498: 'Character not found.'}

    def __call__(self) -> DataPageLogSchema:
        return super().__call__(None)


class GetMyCharacters(SingleArtifactsRequest):
    """
    Get My Characters
    List of your characters.
    operationId: get_my_characters_my_characters_get
    """
    endpoint_pattern = '/my/characters'
    method_name = 'get'
    response_schema = MyCharactersListSchema
    error_responses = {}

    def __call__(self) -> MyCharactersListSchema:
        return super().__call__(None)


class GetBankDetails(SingleArtifactsRequest):
    """
    Get Bank Details
    Fetch bank details.
    operationId: get_bank_details_my_bank_get
    """
    endpoint_pattern = '/my/bank'
    method_name = 'get'
    response_schema = BankResponseSchema
    error_responses = {}

    def __call__(self) -> BankResponseSchema:
        return super().__call__(None)


class GetBankItems(SingleArtifactsRequest):
    """
    Get Bank Items
    Fetch all items in your bank.
    operationId: get_bank_items_my_bank_items_get
    """
    endpoint_pattern = '/my/bank/items'
    method_name = 'get'
    response_schema = DataPageSimpleItemSchema
    error_responses = {}

    def __call__(self) -> DataPageSimpleItemSchema:
        return super().__call__(None)


class GetGeSellOrders(SingleArtifactsRequest):
    """
    Get Ge Sell Orders
    Fetch your sell orders details.
    operationId: get_ge_sell_orders_my_grandexchange_orders_get
    """
    endpoint_pattern = '/my/grandexchange/orders'
    method_name = 'get'
    response_schema = DataPageGEOrderSchema
    error_responses = {}

    def __call__(self) -> DataPageGEOrderSchema:
        return super().__call__(None)


class GetGeSellHistory(SingleArtifactsRequest):
    """
    Get Ge Sell History
    Fetch your sales history of the last 7 days.
    operationId: get_ge_sell_history_my_grandexchange_history_get
    """
    endpoint_pattern = '/my/grandexchange/history'
    method_name = 'get'
    response_schema = DataPageGeOrderHistorySchema
    error_responses = {}

    def __call__(self) -> DataPageGeOrderHistorySchema:
        return super().__call__(None)


class GetAccountDetails(SingleArtifactsRequest):
    """
    Get Account Details
    Fetch account details.
    operationId: get_account_details_my_details_get
    """
    endpoint_pattern = '/my/details'
    method_name = 'get'
    response_schema = MyAccountDetailsSchema
    error_responses = {}

    def __call__(self) -> MyAccountDetailsSchema:
        return super().__call__(None)


class ChangePassword(SingleArtifactsRequest):
    """
    Change Password
    Change your account password. Changing the password reset the account token.
    operationId: change_password_my_change_password_post
    """
    endpoint_pattern = '/my/change_password'
    method_name = 'post'
    response_schema = ResponseSchema
    error_responses = {458: 'Use a different password.'}

    def __call__(self, data: ChangePassword) -> ResponseSchema:
        return super().__call__(data)


class CreateCharacter(SingleArtifactsRequest):
    """
    Create Character
    Create new character on your account. You can create up to 5 characters.
    operationId: create_character_characters_create_post
    """
    endpoint_pattern = '/characters/create'
    method_name = 'post'
    response_schema = CharacterResponseSchema
    error_responses = {494: 'Name already used.',
                       495: 'Maximum characters reached on your account.'}

    def __call__(self, data: AddCharacterSchema) -> CharacterResponseSchema:
        return super().__call__(data)


class DeleteCharacter(SingleArtifactsRequest):
    """
    Delete Character
    Delete character on your account.
    operationId: delete_character_characters_delete_post
    """
    endpoint_pattern = '/characters/delete'
    method_name = 'post'
    response_schema = CharacterResponseSchema
    error_responses = {498: 'Character not found.'}

    def __call__(self, data: DeleteCharacterSchema) -> CharacterResponseSchema:
        return super().__call__(data)


class GetCharacter(CharacterRequest):
    """
    Get Character
    Retrieve the details of a character.
    operationId: get_character_characters__name__get
    """
    endpoint_pattern = '/characters/{name}'
    method_name = 'get'
    response_schema = CharacterResponseSchema
    error_responses = {404: 'Character not found.'}

    def __call__(self) -> CharacterResponseSchema:
        return super().__call__(None)


class GetAllMaps(SingleArtifactsRequest):
    """
    Get All Maps
    Fetch maps details.
    operationId: get_all_maps_maps_get
    """
    endpoint_pattern = '/maps'
    method_name = 'get'
    response_schema = DataPageMapSchema
    error_responses = {}

    def __call__(self) -> DataPageMapSchema:
        return super().__call__(None)


class GetMap(SingleArtifactsRequest):
    """
    Get Map
    Retrieve the details of a map.
    operationId: get_map_maps__x___y__get
    """
    endpoint_pattern = '/maps/{x}/{y}'
    method_name = 'get'
    response_schema = MapResponseSchema
    error_responses = {404: 'Map not found.'}

    def __call__(self) -> MapResponseSchema:
        return super().__call__(None)


class GetAllItems(SingleArtifactsRequest):
    """
    Get All Items
    Fetch items details.
    operationId: get_all_items_items_get
    """
    endpoint_pattern = '/items'
    method_name = 'get'
    response_schema = DataPageItemSchema
    error_responses = {}

    def __call__(self) -> DataPageItemSchema:
        return super().__call__(None)


class GetItem(SingleArtifactsRequest):
    """
    Get Item
    Retrieve the details of a item.
    operationId: get_item_items__code__get
    """
    endpoint_pattern = '/items/{code}'
    method_name = 'get'
    response_schema = ItemResponseSchema
    error_responses = {404: 'Item not found.'}

    def __call__(self) -> ItemResponseSchema:
        return super().__call__(None)


class GetAllMonsters(SingleArtifactsRequest):
    """
    Get All Monsters
    Fetch monsters details.
    operationId: get_all_monsters_monsters_get
    """
    endpoint_pattern = '/monsters'
    method_name = 'get'
    response_schema = DataPageMonsterSchema
    error_responses = {}

    def __call__(self) -> DataPageMonsterSchema:
        return super().__call__(None)


class GetMonster(SingleArtifactsRequest):
    """
    Get Monster
    Retrieve the details of a monster.
    operationId: get_monster_monsters__code__get
    """
    endpoint_pattern = '/monsters/{code}'
    method_name = 'get'
    response_schema = MonsterResponseSchema
    error_responses = {404: 'Monster not found.'}

    def __call__(self) -> MonsterResponseSchema:
        return super().__call__(None)


class GetAllResources(SingleArtifactsRequest):
    """
    Get All Resources
    Fetch resources details.
    operationId: get_all_resources_resources_get
    """
    endpoint_pattern = '/resources'
    method_name = 'get'
    response_schema = DataPageResourceSchema
    error_responses = {}

    def __call__(self) -> DataPageResourceSchema:
        return super().__call__(None)


class GetResource(SingleArtifactsRequest):
    """
    Get Resource
    Retrieve the details of a resource.
    operationId: get_resource_resources__code__get
    """
    endpoint_pattern = '/resources/{code}'
    method_name = 'get'
    response_schema = ResourceResponseSchema
    error_responses = {404: 'Resource not found.'}

    def __call__(self) -> ResourceResponseSchema:
        return super().__call__(None)


class GetAllActiveEvents(SingleArtifactsRequest):
    """
    Get All Active Events
    Fetch active events details.
    operationId: get_all_active_events_events_active_get
    """
    endpoint_pattern = '/events/active'
    method_name = 'get'
    response_schema = DataPageActiveEventSchema
    error_responses = {}

    def __call__(self) -> DataPageActiveEventSchema:
        return super().__call__(None)


class GetAllEvents(SingleArtifactsRequest):
    """
    Get All Events
    Fetch events details.
    operationId: get_all_events_events_get
    """
    endpoint_pattern = '/events'
    method_name = 'get'
    response_schema = DataPageEventSchema
    error_responses = {}

    def __call__(self) -> DataPageEventSchema:
        return super().__call__(None)


class GetGeSellHistory(SingleArtifactsRequest):
    """
    Get Ge Sell History
    Fetch the sales history of the item for the last 7 days.
    operationId: get_ge_sell_history_grandexchange_history__code__get
    """
    endpoint_pattern = '/grandexchange/history/{code}'
    method_name = 'get'
    response_schema = DataPageGeOrderHistorySchema
    error_responses = {404: 'Item not found.'}

    def __call__(self) -> DataPageGeOrderHistorySchema:
        return super().__call__(None)


class GetGeSellOrders(SingleArtifactsRequest):
    """
    Get Ge Sell Orders
    Fetch all sell orders.
    operationId: get_ge_sell_orders_grandexchange_orders_get
    """
    endpoint_pattern = '/grandexchange/orders'
    method_name = 'get'
    response_schema = DataPageGEOrderSchema
    error_responses = {}

    def __call__(self) -> DataPageGEOrderSchema:
        return super().__call__(None)


class GetGeSellOrder(SingleArtifactsRequest):
    """
    Get Ge Sell Order
    Retrieve the sell order of a item.
    operationId: get_ge_sell_order_grandexchange_orders__id__get
    """
    endpoint_pattern = '/grandexchange/orders/{id}'
    method_name = 'get'
    response_schema = GEOrderReponseSchema
    error_responses = {404: 'Order not found.'}

    def __call__(self) -> GEOrderReponseSchema:
        return super().__call__(None)


class GetAllTasks(SingleArtifactsRequest):
    """
    Get All Tasks
    Fetch the list of all tasks.
    operationId: get_all_tasks_tasks_list_get
    """
    endpoint_pattern = '/tasks/list'
    method_name = 'get'
    response_schema = DataPageTaskFullSchema
    error_responses = {}

    def __call__(self) -> DataPageTaskFullSchema:
        return super().__call__(None)


class GetTask(SingleArtifactsRequest):
    """
    Get Task
    Retrieve the details of a task.
    operationId: get_task_tasks_list__code__get
    """
    endpoint_pattern = '/tasks/list/{code}'
    method_name = 'get'
    response_schema = TaskFullResponseSchema
    error_responses = {404: 'Task not found.'}

    def __call__(self) -> TaskFullResponseSchema:
        return super().__call__(None)


class GetAllTasksRewards(SingleArtifactsRequest):
    """
    Get All Tasks Rewards
    Fetch the list of all tasks rewards. To obtain these rewards, you must exchange 6 task coins with a tasks master.
    operationId: get_all_tasks_rewards_tasks_rewards_get
    """
    endpoint_pattern = '/tasks/rewards'
    method_name = 'get'
    response_schema = DataPageDropRateSchema
    error_responses = {}

    def __call__(self) -> DataPageDropRateSchema:
        return super().__call__(None)


class GetTasksReward(SingleArtifactsRequest):
    """
    Get Tasks Reward
    Retrieve the details of a tasks reward.
    operationId: get_tasks_reward_tasks_rewards__code__get
    """
    endpoint_pattern = '/tasks/rewards/{code}'
    method_name = 'get'
    response_schema = TasksRewardResponseSchema
    error_responses = {404: 'Tasks reward not found.'}

    def __call__(self) -> TasksRewardResponseSchema:
        return super().__call__(None)


class GetAllAchievements(SingleArtifactsRequest):
    """
    Get All Achievements
    List of all achievements.
    operationId: get_all_achievements_achievements_get
    """
    endpoint_pattern = '/achievements'
    method_name = 'get'
    response_schema = DataPageAchievementSchema
    error_responses = {}

    def __call__(self) -> DataPageAchievementSchema:
        return super().__call__(None)


class GetAchievement(SingleArtifactsRequest):
    """
    Get Achievement
    Retrieve the details of a achievement.
    operationId: get_achievement_achievements__code__get
    """
    endpoint_pattern = '/achievements/{code}'
    method_name = 'get'
    response_schema = AchievementResponseSchema
    error_responses = {404: 'achievement not found.'}

    def __call__(self) -> AchievementResponseSchema:
        return super().__call__(None)


class GetCharactersLeaderboard(SingleArtifactsRequest):
    """
    Get Characters Leaderboard
    Fetch leaderboard details.
    operationId: get_characters_leaderboard_leaderboard_characters_get
    """
    endpoint_pattern = '/leaderboard/characters'
    method_name = 'get'
    response_schema = DataPageCharacterLeaderboardSchema
    error_responses = {}

    def __call__(self) -> DataPageCharacterLeaderboardSchema:
        return super().__call__(None)


class GetAccountsLeaderboard(SingleArtifactsRequest):
    """
    Get Accounts Leaderboard
    Fetch leaderboard details.
    operationId: get_accounts_leaderboard_leaderboard_accounts_get
    """
    endpoint_pattern = '/leaderboard/accounts'
    method_name = 'get'
    response_schema = DataPageAccountLeaderboardSchema
    error_responses = {}

    def __call__(self) -> DataPageAccountLeaderboardSchema:
        return super().__call__(None)


class CreateAccount(SingleArtifactsRequest):
    """
    Create Account
    None
    operationId: create_account_accounts_create_post
    """
    endpoint_pattern = '/accounts/create'
    method_name = 'post'
    response_schema = ResponseSchema
    error_responses = {456: 'Username already used.',
                       457: 'Email already used.'}

    def __call__(self, data: AddAccountSchema) -> ResponseSchema:
        return super().__call__(data)


class GetAccountAchievements(SingleArtifactsRequest):
    """
    Get Account Achievements
    Retrieve the achievements of a account.
    operationId: get_account_achievements_accounts__account__achievements_get
    """
    endpoint_pattern = '/accounts/{account}/achievements'
    method_name = 'get'
    response_schema = DataPageAccountAchievementSchema
    error_responses = {404: 'Account not found.'}

    def __call__(self) -> DataPageAccountAchievementSchema:
        return super().__call__(None)


class GetAccount(SingleArtifactsRequest):
    """
    Get Account
    Retrieve the details of a character.
    operationId: get_account_accounts__account__get
    """
    endpoint_pattern = '/accounts/{account}'
    method_name = 'get'
    response_schema = AccountDetailsSchema
    error_responses = {404: 'Account not found.'}

    def __call__(self) -> AccountDetailsSchema:
        return super().__call__(None)


class GenerateToken(SingleArtifactsRequest):
    """
    Generate Token
    Use your account as HTTPBasic Auth to generate your token to use the API. You can also generate your token directly on the website.
    operationId: generate_token_token_post
    """
    endpoint_pattern = '/token'
    method_name = 'post'
    response_schema = TokenResponseSchema
    error_responses = {455: 'Token generation failed.'}

    def __call__(self) -> TokenResponseSchema:
        return super().__call__(None)


class GetStatus(SingleArtifactsRequest):
    """
    Get Status
    Return the status of the game server.
    operationId: get_status__get
    """
    endpoint_pattern = '/'
    method_name = 'get'
    response_schema = StatusResponseSchema
    error_responses = {}

    def __call__(self) -> StatusResponseSchema:
        return super().__call__(None)
