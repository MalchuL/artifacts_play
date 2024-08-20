import os

import luigi
from dynaconf import settings
from src.task_manager.luigi.world_task import WorldTask


class CharacterTask(WorldTask):
    datetime = luigi.DateSecondParameter()  # We need time because
    char_name: str = luigi.Parameter()

    @property
    def output_extension(self):
        return "txt"

    @property
    def output_path(self):
        return os.path.join(settings.TASK_OUT_DIRECTORY, self.char_name,
                            f"{self.__class__.__name__}_{self.datetime}.{self.output_extension}")

    def output(self):
        return luigi.LocalTarget(self.output_path)
