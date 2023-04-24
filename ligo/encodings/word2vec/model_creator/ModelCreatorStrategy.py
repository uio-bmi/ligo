import abc
from pathlib import Path

from ligo.data_model.dataset.RepertoireDataset import RepertoireDataset
from ligo.environment.SequenceType import SequenceType


class ModelCreatorStrategy(metaclass=abc.ABCMeta):
    """
    Defines how word2vec model can be created by defining different contexts for k-mers
    """

    def __init__(self, epochs: int, window: int):
        self.epochs = epochs
        self.window = window

    @abc.abstractmethod
    def create_model(self, dataset: RepertoireDataset, k: int, vector_size: int, batch_size: int, model_path: Path, sequence_type: SequenceType):
        pass
