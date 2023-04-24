# quality: gold

import abc
import random
from pathlib import Path

from ligo.data_model.receptor.receptor_sequence.ReceptorSequence import ReceptorSequence
from ligo.data_model.repertoire.Repertoire import Repertoire
from ligo.environment.SequenceType import SequenceType
from ligo.simulation.sequence_implanting.SequenceImplantingStrategy import SequenceImplantingStrategy
from ligo.simulation.signal_implanting.ImplantingComputation import ImplantingComputation


class SignalImplantingStrategy(metaclass=abc.ABCMeta):

    def __init__(self, implanting: SequenceImplantingStrategy = None, sequence_position_weights: dict = None,
                 implanting_computation: ImplantingComputation = None):
        self.sequence_implanting_strategy = implanting
        self.sequence_position_weights = sequence_position_weights
        self.compute_implanting = implanting_computation

    @abc.abstractmethod
    def implant_in_repertoire(self, repertoire: Repertoire, repertoire_implanting_rate: float, signal, path: Path):
        pass

    def implant_in_sequence(self, sequence: ReceptorSequence, signal, motif=None, chain=None, sequence_type: SequenceType = SequenceType.AMINO_ACID) -> ReceptorSequence:
        assert self.sequence_implanting_strategy is not None, \
            "SignalImplanting: set SequenceImplantingStrategy in SignalImplanting object before calling implant_in_sequence method."

        if motif is None:
            motif = random.choice(signal.motifs)

        motif_instance = motif.instantiate_motif(chain)
        new_sequence = self.sequence_implanting_strategy.implant(sequence=sequence,
                                                                 signal={"signal_id": signal.id,
                                                                         "motif_id": motif.identifier,
                                                                         "motif_instance": motif_instance},
                                                                 sequence_position_weights=self.sequence_position_weights,
                                                                 sequence_type=sequence_type)
        return new_sequence

    @abc.abstractmethod
    def implant_in_receptor(self, receptor, signal, is_noise: bool):
        pass
