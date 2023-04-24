from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Set, Dict

from ligo.data_model.dataset.Dataset import Dataset
from ligo.environment.LabelConfiguration import LabelConfiguration
from ligo.hyperparameter_optimization.HPSetting import HPSetting
from ligo.hyperparameter_optimization.config.SplitConfig import SplitConfig
from ligo.hyperparameter_optimization.states.HPAssessmentState import HPAssessmentState
from ligo.hyperparameter_optimization.states.HPItem import HPItem
from ligo.hyperparameter_optimization.strategy.HPOptimizationStrategy import HPOptimizationStrategy
from ligo.ml_metrics.Metric import Metric
from ligo.reports.ReportResult import ReportResult


@dataclass
class TrainMLModelState:
    dataset: Dataset
    hp_strategy: HPOptimizationStrategy
    hp_settings: List[HPSetting]
    assessment: SplitConfig
    selection: SplitConfig
    metrics: Set[Metric]
    optimization_metric: Metric
    label_configuration: LabelConfiguration
    path: Path = None
    context: dict = None
    number_of_processes: int = 1
    reports: dict = field(default_factory=dict)
    name: str = None
    refit_optimal_model: bool = None
    optimal_hp_items: Dict[str, HPItem] = field(default_factory=dict)
    optimal_hp_item_paths: Dict[str, str] = field(default_factory=dict)
    assessment_states: List[HPAssessmentState] = field(default_factory=list)
    report_results: List[ReportResult] = field(default_factory=list)
