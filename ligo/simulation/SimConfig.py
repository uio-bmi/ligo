from dataclasses import dataclass
from typing import List, Union

from ligo.environment.SequenceType import SequenceType
from ligo.simulation.SimConfigItem import SimConfigItem
from ligo.simulation.simulation_strategy.SimulationStrategy import SimulationStrategy


@dataclass
class SimConfig:
    """
    Defines all parameters of the simulation.

    Arguments:

    - sim_items (dict): a list of SimConfigItems defining individual units of simulation

    - is_repertoire (bool): whether the simulation is on a repertoire (person) or sequence/receptor level

    - paired: if the simulation should output paired data, this parameter should contain a list of a list of sim_item pairs referenced by name that should be combined; if paired data is not needed, then it should be False

    - sequence_type (str): either amino_acid or nucleotide

    - simulation_strategy (str): either RejectionSampling or Implanting, see the tutorials for more information on choosing one of these

    - keep_p_gen_dist (bool): if possible, whether to keep the distribution of generation probabilities of the sequences the same as provided by the model without any signals

    - p_gen_bin_count (int): if keep_p_gen_dist is true, how many bins to use to approximate the generation probability distribution

    - remove_seqs_with_signals (bool): if true, it explicitly controls the proportions of signals in sequences and removes any accidental occurrences

    - species (str): species that the sequences come from; used to select correct genes to export full length sequences; default is 'human'

    - implanting_scaling_factor (int): determines in how many receptors to implant the signal in reach iteration; this is computed as number_of_receptors_needed_for_signal * implanting_scaling_factor; useful when using Implanting simulation strategy in combination with importance sampling, since the generation probability of some receptors with implanted signals might be very rare and those receptors might end up not being kept often with importance sampling; this parameter is only used when keep_p_gen_dist is set to True

    YAML specification:

    .. code-block:: yaml

      simulations:
        sim1:
          is_repertoire: false
          paired: false
          sequence_type: amino_acid
          simulation_strategy: RejectionSampling
          sim_items:
            sim_item1: # group of sequences with same simulation params
              generative_model:
                chain: beta
                default_model_name: humanTRB
                model_path: null
                type: OLGA
              number_of_examples: 100
              seed: 1002
              signals:
               signal1: 1

    """
    sim_items: List[SimConfigItem] = None
    identifier: str = None
    is_repertoire: bool = None
    paired: Union[bool, List[List[str]]] = None
    sequence_type: SequenceType = None
    simulation_strategy: SimulationStrategy = None
    p_gen_bin_count: int = None
    keep_p_gen_dist: bool = None
    remove_seqs_with_signals: bool = None
    species: str = None
    implanting_scaling_factor: int = None

    def __str__(self):
        return ",\n".join(str(simulation_item) for simulation_item in self.sim_items)
