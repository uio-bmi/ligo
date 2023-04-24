# quality: gold

import abc
from pathlib import Path

from ligo.data_model.dataset.Dataset import Dataset
from ligo.data_model.receptor.RegionType import RegionType


class DataExporter(metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def export(dataset: Dataset, path: Path, number_of_processes: int = 1):
        pass
