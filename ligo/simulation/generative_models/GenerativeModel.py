import abc
from pathlib import Path

import numpy as np

from ligo.environment.SequenceType import SequenceType


class GenerativeModel:

    OUTPUT_COLUMNS = []

    def __init__(self, chain):
        self.chain = chain
        self.region_type = None

    @abc.abstractmethod
    def is_same(self, model) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def generate_sequences(self, count: int, seed: int, path: Path, sequence_type: SequenceType, compute_p_gen: bool):
        pass

    @abc.abstractmethod
    def compute_p_gens(self, sequences, sequence_type: SequenceType, sequence_field: str = None) -> np.ndarray:
        pass

    @abc.abstractmethod
    def compute_p_gen(self, sequence: dict, sequence_type: SequenceType, sequence_field: str = None) -> float:
        pass

    @abc.abstractmethod
    def can_compute_p_gens(self) -> bool:
        pass

    @abc.abstractmethod
    def can_generate_from_skewed_gene_models(self) -> bool:
        pass

    @abc.abstractmethod
    def generate_from_skewed_gene_models(self, v_genes: list, j_genes: list, seed: int, path: Path, sequence_type: SequenceType, batch_size: int,
                                         compute_p_gen: bool):
        pass
