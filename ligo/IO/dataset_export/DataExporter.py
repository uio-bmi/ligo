# quality: gold

import abc
from pathlib import Path

from ligo.data_model.dataset.Dataset import Dataset


class DataExporter(metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def export(dataset: Dataset, path: Path, number_of_processes: int = 1, omit_columns: list = None):
        pass
