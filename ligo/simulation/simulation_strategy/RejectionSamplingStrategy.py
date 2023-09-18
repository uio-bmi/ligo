from typing import List

from bionumpy.bnpdataclass import BNPDataClass

from ligo.environment.SequenceType import SequenceType
from ligo.simulation.SimConfigItem import SimConfigItem
from ligo.simulation.implants.Signal import Signal
from ligo.simulation.simulation_strategy.SimulationStrategy import SimulationStrategy
from ligo.simulation.util.util import filter_out_illegal_sequences
from ligo.util.Logger import print_log


class RejectionSamplingStrategy(SimulationStrategy):

    MAX_SIGNALS_PER_SEQUENCE = 2
    MAX_MOTIFS_PER_SEQUENCE = 1

    def process_sequences(self, sequences: BNPDataClass, seqs_per_signal_count: dict, use_p_gens: bool,
                          sequence_type: SequenceType, sim_item: SimConfigItem, all_signals: List[Signal],
                          remove_positives_first: bool, **kwargs) -> BNPDataClass:

        filtered_sequences = filter_out_illegal_sequences(sequences, sim_item, all_signals,
                                                          RejectionSamplingStrategy.MAX_SIGNALS_PER_SEQUENCE,
                                                          RejectionSamplingStrategy.MAX_MOTIFS_PER_SEQUENCE)

        removed_count = len(sequences) - len(filtered_sequences)
        if removed_count > 0:
            print_log(f"Removed {removed_count} out of {len(sequences)} during rejection sampling for having "
                      f"more than 1 signal.", True)

        return filtered_sequences
