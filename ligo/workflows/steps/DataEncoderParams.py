from dataclasses import dataclass

from ligo.data_model.dataset.Dataset import Dataset
from ligo.encodings.DatasetEncoder import DatasetEncoder
from ligo.encodings.EncoderParams import EncoderParams
from ligo.workflows.steps.StepParams import StepParams


@dataclass
class DataEncoderParams(StepParams):

    dataset: Dataset
    encoder: DatasetEncoder
    encoder_params: EncoderParams
