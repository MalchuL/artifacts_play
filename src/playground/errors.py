from abc import ABC


class ArtifactsException(Exception):
    ERROR_CODE = None
    ERROR_MESSAGE = None

    def __init__(self, *args):
        message = self.ERROR_MESSAGE
        if args:
            message = args
        super().__init__(message)

    @property
    def error_code(self):
        return self.ERROR_CODE

    @property
    def error_message(self):
        return self.ERROR_MESSAGE


class CharacterInventoryFullException(ArtifactsException):
    ERROR_CODE = 497
    ERROR_MESSAGE = "Character inventory is full."


class MissingItemOrInsufficientQuantityException(ArtifactsException):
    ERROR_CODE = 478
    ERROR_MESSAGE = "Missing item or insufficient quantity in your inventory."


class UnspecifiedException(ArtifactsException):
    ERROR_CODE = 1
    ERROR_MESSAGE = "Unspecified error."


ERRORS_MAPPING = {
    error.ERROR_CODE: error for error in [CharacterInventoryFullException,
                                          MissingItemOrInsufficientQuantityException]
}
