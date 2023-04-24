import abc

from ligo.data_model.receptor.receptor_sequence.ReceptorSequence import ReceptorSequence
from ligo.environment.SequenceType import SequenceType


class SequenceImplantingStrategy(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def implant(self, sequence: ReceptorSequence, signal: dict, sequence_position_weights, sequence_type: SequenceType = SequenceType.AMINO_ACID)\
        -> ReceptorSequence:
        pass
