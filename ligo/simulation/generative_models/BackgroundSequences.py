from typing import List

from bionumpy import AminoAcidEncoding, DNAEncoding
from bionumpy.bnpdataclass import bnpdataclass

from ligo.data_model.receptor.receptor_sequence.ReceptorSequence import ReceptorSequence
from ligo.environment.SequenceType import SequenceType


@bnpdataclass
class BackgroundSequences:
    sequence_aa: AminoAcidEncoding
    sequence: DNAEncoding
    v_call: str
    j_call: str
    region_type: str
    frame_type: str
    p_gen: float
    from_default_model: int
    duplicate_count: int
    chain: str

    def get_sequence(self, sequence_type: SequenceType = SequenceType.AMINO_ACID):
        if sequence_type == SequenceType.AMINO_ACID:
            return self.sequence_aa
        else:
            return self.sequence

    @classmethod
    def build_from_receptor_sequences(cls, sequences: List[ReceptorSequence]):
        return BackgroundSequences(sequence_aa=[s.amino_acid_sequence for s in sequences],
                                   sequence=[s.nucleotide_sequence for s in sequences],
                                   v_call=[s.metadata.v_call if s.metadata else '' for s in sequences],
                                   j_call=[s.metadata.j_call if s.metadata else '' for s in sequences],
                                   region_type=[s.metadata.region_type.name if s.metadata and s.metadata.region_type
                                                else '' for s in sequences],
                                   frame_type=[s.metadata.frame_type.name if s.metadata and s.metadata.frame_type
                                               else '' for s in sequences],
                                   p_gen=[-1. for _ in sequences], from_default_model=[1 for _ in sequences],
                                   duplicate_count=[s.metadata.duplicate_count if s.metadata.duplicate_count is not None else -1 for s in sequences],
                                   chain=[s.metadata.chain.value for s in sequences])
