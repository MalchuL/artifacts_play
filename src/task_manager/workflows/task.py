import copy
import logging
from abc import abstractmethod, ABC
from typing import Any, Dict


class Rerun(Exception):
    pass


class Task(ABC):
    def __init__(self):
        self._outs = {}
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.propagate = True

    @property
    def logger(self) -> logging.Logger:
        return self._logger

    @abstractmethod
    def run(self):
        pass

    def outputs(self) -> Dict[str, Any]:
        return self._outs

    def start(self):
        while True:
            try:
                self._outs = {}
                self.run()
                break
            except Rerun as e:
                self.logger.info(f"Rerun {self.__class__.__name__}, {e}")
        return self.outputs()
