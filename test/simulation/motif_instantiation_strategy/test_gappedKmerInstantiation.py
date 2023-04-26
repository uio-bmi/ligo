import os
from unittest import TestCase

from ligo.environment.Constants import Constants
from ligo.environment.SequenceType import SequenceType
from ligo.simulation.motif_instantiation_strategy.GappedKmerInstantiation import GappedKmerInstantiation


class TestGappedKmerInstantiation(TestCase):

    alphabet_weights = {"T": 0.5, "F": 0.5, "A": 0, "C": 0, "D": 0, "E": 0, "G": 0, "H": 0, "K": 0, "I": 0, "L": 0, "M": 0,
                        "N": 0, "P": 0, "Q": 0, "R": 0, "S": 0, "V": 0, "W": 0, "Y": 0}

    def test_instantiate_motif(self):

        strategy = GappedKmerInstantiation(hamming_distance_probabilities={0: 0.333, 1: 0.333, 2: 0.333}, max_gap=2, min_gap=1,
                                           position_weights={0: 1, 1: 1, 2: 0, 3: 0},
                                           alphabet_weights=self.alphabet_weights)

        instance = strategy.instantiate_motif("C/AS")

        self.assertTrue("AS" in instance.instance)
        self.assertEqual(len(instance.instance), 4)
        self.assertTrue(1 <= instance.gap <= 2)
        self.assertTrue(instance.instance[0] in ["C", "T", "F"])

        strategy = GappedKmerInstantiation(hamming_distance_probabilities={0: 0.5, 1: 0.5},
                                           position_weights={0: 1, 1: 0, 2: 0},
                                           alphabet_weights=self.alphabet_weights)

        instance = strategy.instantiate_motif("CAS")

        self.assertTrue("AS" in instance.instance)
        self.assertEqual(len(instance.instance), 3)
        self.assertTrue(instance.gap == 0)
        self.assertTrue(instance.instance[0] in ["C", "T", "F"])

        strategy = GappedKmerInstantiation(hamming_distance_probabilities={0: 0.333, 1: 0.333, 2: 0.333},
                                           position_weights=None, alphabet_weights=None)

        strategy.instantiate_motif("CAS")

    def test_get_all_possible_motifs(self):

        strategy = GappedKmerInstantiation(hamming_distance_probabilities={0: 0.0, 1: 0.667, 2: 0.333}, max_gap=1, min_gap=0,
                                           position_weights={0: 1, 1: 1},
                                           alphabet_weights=self.alphabet_weights)

        instances = strategy.get_all_possible_instances("SQ", SequenceType.AMINO_ACID)

        self.assertListEqual(instances, ['[FT]Q', 'S[FT]', '[FT][FT]'])

        strategy.position_weights = {0: 1, 1: 1, 2: 1}
        instances = strategy.get_all_possible_instances("S/Q", SequenceType.AMINO_ACID)
        self.assertListEqual(instances, ['[FT].{0,1}Q', 'S.{0,1}[FT]', '[FT].{0,1}[FT]'])
