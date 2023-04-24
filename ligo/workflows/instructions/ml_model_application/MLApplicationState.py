from dataclasses import dataclass
from pathlib import Path

from ligo.data_model.dataset.Dataset import Dataset
from ligo.environment.LabelConfiguration import LabelConfiguration
from ligo.hyperparameter_optimization.HPSetting import HPSetting


@dataclass
class MLApplicationState:

    dataset: Dataset
    hp_setting: HPSetting
    label_config: LabelConfiguration
    pool_size: int
    name: str
    metrics: list = None
    path: Path = None
    predictions_path: Path = None
    metrics_path: Path = None
