from dataclasses import dataclass
from pathlib import Path
from typing import List

from ligo.data_model.dataset.Dataset import Dataset
from ligo.preprocessing.Preprocessor import Preprocessor


@dataclass
class DatasetExportState:
    datasets: List[Dataset]
    formats: List[str]
    preprocessing_sequence: List[Preprocessor]
    paths: dict
    result_path: Path
    name: str
