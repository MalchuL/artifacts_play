from abc import abstractmethod
from dataclasses import dataclass


@dataclass
class Update:
    pass


@abstractmethod
class Updatable:  # abstract class for updatable objects.
    def update(self, update: Update):
        """Method to update the object.

        It is called by the game loop.
        :param update:
        :return:
        """
        pass
