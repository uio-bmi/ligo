from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from ligo.data_model.dataset.Dataset import Dataset
from ligo.encodings.DatasetEncoder import DatasetEncoder
from ligo.hyperparameter_optimization.HPSetting import HPSetting
from ligo.ml_methods.MLMethod import MLMethod
from ligo.reports.ReportResult import ReportResult


@dataclass
class HPItem:

    method: MLMethod = None
    encoder: DatasetEncoder = None
    performance: dict = None
    hp_setting: HPSetting = None
    train_predictions_path: Path = None
    test_predictions_path: Path = None
    ml_details_path: Path = None
    train_dataset: Dataset = None
    test_dataset: Dataset = None
    split_index: int = None
    model_report_results: List[ReportResult] = field(default_factory=list)
    encoding_train_results: List[ReportResult] = field(default_factory=list)
    encoding_test_results: List[ReportResult] = field(default_factory=list)
