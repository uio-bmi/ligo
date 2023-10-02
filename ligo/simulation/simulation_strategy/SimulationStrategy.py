import abc
from typing import List

from bionumpy.bnpdataclass import BNPDataClass

from ligo.environment.SequenceType import SequenceType
from ligo.simulation.SimConfigItem import SimConfigItem
from ligo.simulation.implants.Signal import Signal


class SimulationStrategy:

    @abc.abstractmethod
    def process_sequences(self, sequences: BNPDataClass, seqs_per_signal_count: dict, use_p_gens: bool,
                          sequence_type: SequenceType, sim_item: SimConfigItem, all_signals: List[Signal],
                          remove_positives_first: bool, **kwargs) -> BNPDataClass:
        pass
