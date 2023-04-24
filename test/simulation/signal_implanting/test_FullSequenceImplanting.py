import shutil
from unittest import TestCase

from ligo.data_model.receptor.RegionType import RegionType
from ligo.data_model.repertoire.Repertoire import Repertoire
from ligo.environment.EnvironmentSettings import EnvironmentSettings
from ligo.simulation.implants.Motif import Motif
from ligo.simulation.implants.Signal import Signal
from ligo.simulation.motif_instantiation_strategy.GappedKmerInstantiation import GappedKmerInstantiation
from ligo.simulation.signal_implanting.FullSequenceImplanting import FullSequenceImplanting
from ligo.util.PathBuilder import PathBuilder


class TestFullSequenceImplanting(TestCase):
    def test_implant_in_repertoire(self):
        path = PathBuilder.build(EnvironmentSettings.tmp_test_path / "full_seq_implanting/")
        signal = Signal("sig1", [Motif("motif1", GappedKmerInstantiation(max_gap=0), "AAAA", v_call="v1", j_call="j1")],
                        FullSequenceImplanting())

        repertoire = Repertoire.build(["CCCC", "CCCC", "CCCC"], region_type=[RegionType.IMGT_JUNCTION for _ in range(3)], path=path)

        new_repertoire = signal.implant_to_repertoire(repertoire, 0.33, path)

        self.assertEqual(len(repertoire.sequences), len(new_repertoire.sequences))
        self.assertEqual(1, len([seq for seq in new_repertoire.sequences if seq.amino_acid_sequence == "AAAA" and seq.metadata.v_call == "v1"]))
        self.assertEqual(2, len([seq for seq in new_repertoire.sequences if seq.amino_acid_sequence == "CCCC" and seq.metadata.v_call != "v1"]))
        self.assertEqual(new_repertoire.get_region_type(), RegionType.IMGT_JUNCTION)

        shutil.rmtree(path)
