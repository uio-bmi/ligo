from unittest import TestCase

from ligo.data_model.receptor.receptor_sequence.ReceptorSequence import ReceptorSequence
from ligo.data_model.receptor.receptor_sequence.SequenceMetadata import SequenceMetadata
from ligo.encodings.EncoderParams import EncoderParams
from ligo.encodings.kmer_frequency.sequence_encoding.IdentitySequenceEncoder import IdentitySequenceEncoder
from ligo.environment.LabelConfiguration import LabelConfiguration


class TestIdentitySequenceEncoder(TestCase):
    def test_encode_sequence(self):
        sequence = ReceptorSequence(amino_acid_sequence="AAA", metadata=SequenceMetadata(frame_type="OUT"))
        enc = IdentitySequenceEncoder()
        self.assertEqual(enc.encode_sequence(sequence, EncoderParams(model={},
                                                                     label_config=LabelConfiguration(),
                                                                     result_path="")),
                         ["AAA"])

        sequence = ReceptorSequence(amino_acid_sequence="AAA", metadata=SequenceMetadata(frame_type="STOP"))
        enc = IdentitySequenceEncoder()
        self.assertEqual(enc.encode_sequence(sequence, EncoderParams(model={},
                                                                     label_config=LabelConfiguration(),
                                                                     result_path="")),
                         ["AAA"])

        sequence = ReceptorSequence(amino_acid_sequence="AAA", metadata=SequenceMetadata(frame_type="IN"))
        enc = IdentitySequenceEncoder()
        self.assertEqual(["AAA"],
                         enc.encode_sequence(sequence, EncoderParams(model={},
                                                                     label_config=LabelConfiguration(),
                                                                     result_path="")))
