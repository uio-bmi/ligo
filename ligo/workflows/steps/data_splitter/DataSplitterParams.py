from dataclasses import dataclass

from ligo.data_model.dataset.Dataset import Dataset
from ligo.environment.LabelConfiguration import LabelConfiguration
from ligo.hyperparameter_optimization.config.SplitConfig import SplitConfig
from ligo.hyperparameter_optimization.config.SplitType import SplitType
from ligo.workflows.steps.StepParams import StepParams


@dataclass
class DataSplitterParams(StepParams):

    dataset: Dataset
    split_strategy: SplitType
    split_count: int
    training_percentage: float = -1
    paths: list = None
    split_config: SplitConfig = None
    label_config: LabelConfiguration = None
