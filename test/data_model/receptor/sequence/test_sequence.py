from unittest import TestCase

from ligo.data_model.receptor.receptor_sequence.ReceptorSequence import ReceptorSequence
from ligo.environment.EnvironmentSettings import EnvironmentSettings
from ligo.environment.SequenceType import SequenceType


class TestSequence(TestCase):
    def test_get_sequence(self):

        sequence = ReceptorSequence(amino_acid_sequence="CAS",
                                    nucleotide_sequence="TGTGCTTCC")

        EnvironmentSettings.set_sequence_type(SequenceType.AMINO_ACID)

        self.assertEqual(sequence.get_sequence(), "CAS")
