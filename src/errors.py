class ArtifactsException(Exception):
    ERROR_MESSAGE = None

    def __init__(self, *args):
        message = self.ERROR_MESSAGE
        if args:
            message = args
        super().__init__(message)

    @property
    def error_message(self):
        return self.ERROR_MESSAGE


class UnspecifiedException(ArtifactsException):
    ERROR_CODE = 1
    ERROR_MESSAGE = "Unspecified error."


class NotFoundException(ArtifactsException):
    ERROR_MESSAGE = "Not found."


class ActionInProgressException(ArtifactsException):
    ERROR_MESSAGE = "An action is already in progress by your character."


class CharacterAlreadyAtDestinationException(ArtifactsException):
    ERROR_MESSAGE = "Character already at destination."


class CharacterNotFoundException(ArtifactsException):
    ERROR_MESSAGE = "Character not found."


class CharacterInCooldownException(ArtifactsException):
    ERROR_MESSAGE = "Character in cooldown."


class MissingItemOrInsufficientQuantityException(ArtifactsException):
    ERROR_MESSAGE = "Missing item or insufficient quantity in your inventory."


class ItemAlreadyEquippedException(ArtifactsException):
    ERROR_MESSAGE = "This item is already equipped."


class SlotIsNotEmptyException(ArtifactsException):
    ERROR_MESSAGE = "Slot is not empty."


class CharacterLevelIsInsufficientException(ArtifactsException):
    ERROR_MESSAGE = "Character level is insufficient."


class CharacterInventoryFullException(ArtifactsException):
    ERROR_MESSAGE = "Character inventory is full."


class LocationNotFoundOnMapException(ArtifactsException):
    ERROR_MESSAGE = "Monster/Location not found on this map."


class HigherSkillLevelRequired(ArtifactsException):
    ERROR_MESSAGE = 'Not skill level required.'


class TransactionAlreadyInProgress(ArtifactsException):
    ERROR_MESSAGE = "A transaction is already in progress with this item/your golds in your bank."


class InsufficientGoldsOnCharacter(ArtifactsException):
    ERROR_MESSAGE = 'Insufficient golds on your character.'


class ItemCannotBeRecycleException(ArtifactsException):
    ERROR_MESSAGE = "This item cannot be recycled."


class NoItemAtThisPriceException(ArtifactsException):
    ERROR_MESSAGE = "No item at this price."


class CharacterAlreadyHasATaskException(ArtifactsException):
    ERROR_MESSAGE = "Character already has a task."


class CharacterHasNotCompletedTheTaskException(ArtifactsException):
    ERROR_MESSAGE = "Character has not completed the task."


STATUS_CODE_TO_EXCEPTION = {404: NotFoundException,
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
