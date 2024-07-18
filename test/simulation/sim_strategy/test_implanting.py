from ligo.environment.SequenceType import SequenceType
from ligo.simulation.SimConfigItem import SimConfigItem
from ligo.simulation.generative_models.BackgroundSequences import BackgroundSequences
from ligo.simulation.implants.SeedMotif import SeedMotif
from ligo.simulation.implants.Signal import Signal
from ligo.simulation.simulation_strategy.ImplantingStrategy import ImplantingStrategy


def test_implanting():
    s1 = Signal('s1', [SeedMotif('m1', 'AAA')], {'104': 0, '105': 0})
    seqs = BackgroundSequences(sequence=["CCCCC", "CCCCCCCCC"], sequence_aa=["A", "AA"], v_call=["", ""], j_call=["", ""],
                               region_type=["IMGT_JUNCTION", "IMGT_JUNCTION"], frame_type=["", ""], p_gen=[-1., -1.], from_default_model=[1, 1],
                               duplicate_count=[1,1], chain=["TRB", "TRB"])

    processed_seqs = ImplantingStrategy().process_sequences(seqs, {'s1': 2}, False, SequenceType.NUCLEOTIDE,
                                                            SimConfigItem({s1: 1.}), [s1], False)

    print(processed_seqs)
