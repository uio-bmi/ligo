from pathlib import Path

from ligo.dsl import Util
from ligo.dsl.symbol_table.SymbolTable import SymbolTable
from ligo.dsl.symbol_table.SymbolType import SymbolType
from ligo.util.ParameterValidator import ParameterValidator
from ligo.workflows.instructions.SimulationInstruction import SimulationInstruction


class SimulationParser:
    """

    YAML specification:

    .. highlight:: yaml
    .. code-block:: yaml

        definitions:
            dataset:
                my_dataset:
                    ...

            motifs:
                m1:
                    seed: AAC # "/" character denotes the gap in the seed if present (e.g. AA/C)
                    instantiation:
                        GappedKmer:
                            # probability that when hamming distance is allowed a letter in the seed will be replaced by
                            # other alphabet letters - alphabet_weights
                            alphabet_weights:
                                A: 0.2
                                C: 0.2
                                D: 0.4
                                E: 0.2
                            # Relative probabilities of choosing each position in the seed for hamming distance modification.
                            # The probabilities will be scaled to sum to one - position_weights
                            position_weights:
                                0: 1
                                1: 0
                                2: 0
                            hamming_distance_probabilities:
                                0: 0.5 # Hamming distance of 0 (no change) with probability 0.5
                                1: 0.5 # Hamming distance of 1 (one letter change) with probability 0.5
                            min_gap: 0
                            max_gap: 1
            signals:
                s1:
                    motifs: # list of all motifs for signal which will be uniformly sampled to get a motif instance for implanting
                        - m1
                    sequence_position_weights: # likelihood of implanting at IMGT position of receptor sequence
                        107: 0.5
                    implanting: HealthySequence # choose only sequences with no other signals for to implant one of the motifs
            simulations:
                sim1: # one Simulation object consists of a dict of Implanting objects
                    i1:
                        dataset_implanting_rate: 0.5 # percentage of repertoire where the signals will be implanted
                        repertoire_implanting_rate: 0.01 # percentage of sequences within repertoire where the signals will be implanted
                        signals:
                            - s1

        instructions:
            my_simulation_instruction:
                type: Simulation
                dataset: my_dataset
                simulation: sim1
                export_formats: [AIRR, ImmuneML]

    """

    def parse(self, key: str, instruction: dict, symbol_table: SymbolTable, path: Path = None) -> SimulationInstruction:
        ParameterValidator.assert_keys(instruction.keys(), ["dataset", "simulation", "type", "export_formats", "store_signal_in_receptors"],
                                       "SimulationParser", key)
        ParameterValidator.assert_type_and_value(instruction['store_signal_in_receptors'], bool, key, 'store_signal_in_receptors')

        signals = [signal.item for signal in symbol_table.get_by_type(SymbolType.SIGNAL)]
        simulation = symbol_table.get(instruction["simulation"])
        dataset = symbol_table.get(instruction["dataset"])

        exporters = Util.parse_exporters(instruction, SimulationParser.__name__)

        process = SimulationInstruction(signals=signals, simulation=simulation, dataset=dataset, name=key, exporters=exporters,
                                        store_signal_in_receptors=instruction['store_signal_in_receptors'])
        return process
