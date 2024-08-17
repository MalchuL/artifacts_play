from src.playground.errors import LocationNotFoundOnMapException, CharacterInCooldownException, \
    CharacterNotFoundException, CharacterInventoryFullException, \
    CharacterLevelIsInsufficientException, HigherSkillLevelRequired, InsufficientGoldsOnCharacter, \
    SlotIsNotEmptyException, CharacterAlreadyAtDestinationException, \
    CharacterAlreadyHasATaskException, CharacterHasNotCompletedTheTaskException, \
    ActionInProgressException, ItemAlreadyEquippedException, NoItemAtThisPriceException, \
    MissingItemOrInsufficientQuantityException, ItemCannotBeRecycleException, \
    TransactionAlreadyInProgress, NotFoundException
from src.rest_api_client.errors import ArtifactsHTTPStatusError

CHARACTER_STATUS_CODE_TO_EXCEPTION = {404: NotFoundException,
                                      461: TransactionAlreadyInProgress,
                                      473: ItemCannotBeRecycleException,
                                      478: MissingItemOrInsufficientQuantityException,
                                      482: NoItemAtThisPriceException,
                                      485: ItemAlreadyEquippedException,
                                      486: ActionInProgressException,
                                      488: CharacterHasNotCompletedTheTaskException,
                                      489: CharacterAlreadyHasATaskException,
                                      490: CharacterAlreadyAtDestinationException,
                                      491: SlotIsNotEmptyException,
                                      492: InsufficientGoldsOnCharacter,
                                      493: HigherSkillLevelRequired,
                                      496: CharacterLevelIsInsufficientException,
                                      497: CharacterInventoryFullException,
                                      498: CharacterNotFoundException,
                                      499: CharacterInCooldownException,
                                      598: LocationNotFoundOnMapException}


def char_exception_handler(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except ArtifactsHTTPStatusError as e:
            if e.status_code in CHARACTER_STATUS_CODE_TO_EXCEPTION:
                new_error = CHARACTER_STATUS_CODE_TO_EXCEPTION[e.status_code]
                raise new_error(f"{new_error.ERROR_MESSAGE} from status code ({e.status_code}). {e.content}") from e
            else:
                raise e from e

    return wrapper
