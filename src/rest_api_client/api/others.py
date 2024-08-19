
from ..model import DataPageMapSchema, SimpleItemSchema, MonsterResponseSchema, \
    MyCharactersListSchema, GETransactionItemSchema, GoldResponseSchema, \
    CharacterFightResponseSchema, EquipSchema, DepositWithdrawGoldSchema, ChangePassword, \
    ResponseSchema, DataPageActiveEventSchema, RecyclingResponseSchema, DataPageResourceSchema, \
    DeleteCharacterSchema, GoldBankResponseSchema, DataPageItemSchema, StatusResponseSchema, \
    ItemResponseSchema, AddAccountSchema, DataPageLogSchema, TaskResponseSchema, RecyclingSchema, \
    CraftingSchema, ResourceResponseSchema, TokenResponseSchema, UnequipSchema, \
    DataPageGEItemSchema, EquipmentResponseSchema, MapResponseSchema, DataPageCharacterSchema, \
    ActionItemBankResponseSchema, CharacterResponseSchema, DataPageSimpleItemSchema, \
    SkillResponseSchema, GETransactionResponseSchema, AddCharacterSchema, DataPageMonsterSchema, \
    TaskRewardResponseSchema, DeleteItemResponseSchema, GEItemResponseSchema, DestinationSchema, \
    CharacterMovementResponseSchema

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
    error_responses = {404: 'Characters not found.'}

    def __call__(self) -> MyCharactersListSchema:
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
    error_responses = {404: 'Items not found.'}

    def __call__(self) -> DataPageSimpleItemSchema:
        return super().__call__(None)


class GetBankGolds(SingleArtifactsRequest):
    """
    Get Bank Golds
    Fetch golds in your bank.
    operationId: get_bank_golds_my_bank_gold_get
    """
    endpoint_pattern = '/my/bank/gold'
    method_name = 'get'
    response_schema = GoldBankResponseSchema
    error_responses = {}

    def __call__(self) -> GoldBankResponseSchema:
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


class GetAllCharacters(SingleArtifactsRequest):
    """
    Get All Characters
    Fetch characters details.
    operationId: get_all_characters_characters__get
    """
    endpoint_pattern = '/characters/'
    method_name = 'get'
    response_schema = DataPageCharacterSchema
    error_responses = {404: 'Characters not found.'}

    def __call__(self) -> DataPageCharacterSchema:
        return super().__call__(None)








class GetAllEvents(SingleArtifactsRequest):
    """
    Get All Events
    Fetch events details.
    operationId: get_all_events_events__get
    """
    endpoint_pattern = '/events/'
    method_name = 'get'
    response_schema = DataPageActiveEventSchema
    error_responses = {404: 'Events not found.'}

    def __call__(self) -> DataPageActiveEventSchema:
        return super().__call__(None)


class GetAllGeItems(SingleArtifactsRequest):
    """
    Get All Ge Items
    Fetch Grand Exchange items details.
    operationId: get_all_ge_items_ge__get
    """
    endpoint_pattern = '/ge/'
    method_name = 'get'
    response_schema = DataPageGEItemSchema
    error_responses = {404: 'Item not found.'}

    def __call__(self) -> DataPageGEItemSchema:
        return super().__call__(None)


class GetGeItem(SingleArtifactsRequest):
    """
    Get Ge Item
    Retrieve the details of a Grand Exchange item.
    operationId: get_ge_item_ge__code__get
    """
    endpoint_pattern = '/ge/{code}'
    method_name = 'get'
    response_schema = GEItemResponseSchema
    error_responses = {404: 'Item not found.'}

    def __call__(self) -> GEItemResponseSchema:
        return super().__call__(None)


class CreateAccount(SingleArtifactsRequest):
    """
    Create Account
    Create an account.
    operationId: create_account_accounts_create_post
    """
    endpoint_pattern = '/accounts/create'
    method_name = 'post'
    response_schema = ResponseSchema
    error_responses = {456: 'Username already used.',
                       457: 'Email already used.'}

    def __call__(self, data: AddAccountSchema) -> ResponseSchema:
        return super().__call__(data)


class GenerateToken(SingleArtifactsRequest):
    """
    Generate Token
    Use your account as HTTPBasic Auth to generate your token to use the API. You can also generate your token directly on the website.
    operationId: generate_token_token__post
    """
    endpoint_pattern = '/token/'
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
