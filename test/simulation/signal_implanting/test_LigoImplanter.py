import shutil
from unittest import TestCase

from ligo.simulation.LIgOSimulationItem import SimConfigItem
from ligo.simulation.signal_implanting.LigoImplanter import LigoImplanter
from ligo.simulation.signal_implanting.LigoImplanterState import LigoImplanterState

from ligo.data_model.receptor.receptor_sequence.ReceptorSequence import ReceptorSequence
from ligo.data_model.repertoire.Repertoire import Repertoire
from ligo.environment.EnvironmentSettings import EnvironmentSettings
from ligo.environment.SequenceType import SequenceType
from ligo.simulation.generative_models.OLGA import OLGA
from ligo.simulation.implants.Motif import Motif
from ligo.simulation.implants.Signal import Signal
from ligo.simulation.motif_instantiation_strategy.GappedKmerInstantiation import GappedKmerInstantiation
from ligo.util.PathBuilder import PathBuilder


class TestLigoImplanter(TestCase):

    def test_make_repertoires(self):
        path = PathBuilder.remove_old_and_build(EnvironmentSettings.tmp_test_path / 'ligo_implanter')

        signals = [Signal('s1', [Motif('m1', GappedKmerInstantiation(), 'AA')], {})]
        implanter = LigoImplanter(state=LigoImplanterState(SimConfigItem(signals=signals, name='sim_item1', repertoire_implanting_rate=0.3,
                                                                         is_noise=False, seed=1,
                                                                         generative_model=OLGA.build_object(
                                                                                  **{"default_model_name": 'humanTRB', 'model_path': None,
                                                                                     'use_only_productive': False}),
                                                                         number_of_examples=5, receptors_in_repertoire_count=20),
                                                           sequence_type=SequenceType.AMINO_ACID, all_signals=signals,
                                                           sequence_batch_size=100, seed=1, export_p_gens=True, keep_p_gen_dist=True,
                                                           remove_seqs_with_signals=True,
                                                           max_iterations=100, p_gen_bin_count=5))
        repertoires = implanter.make_repertoires(path)

        self.assertEqual(len(repertoires), 5)
        for repertoire in repertoires:
            self.assertTrue(isinstance(repertoire, Repertoire))
            self.assertEqual(len(repertoire.sequences), 20)
            self.assertTrue(all(repertoire.get_attribute("p_gen") > 0))

        shutil.rmtree(path)

    def test_make_sequences(self):
        path = PathBuilder.remove_old_and_build(EnvironmentSettings.tmp_test_path / 'ligo_implanter_sequences')

        signals = [Signal('s1', [Motif('m1', GappedKmerInstantiation(), 'AA')], {})]
        implanter = LigoImplanter(state=LigoImplanterState(SimConfigItem(signals=signals, name='sim_item1', repertoire_implanting_rate=0,
                                                                         is_noise=False, seed=1,
                                                                         generative_model=OLGA.build_object(
                                                                                  **{"default_model_name": 'humanTRB', 'model_path': None,
                                                                                     'use_only_productive': False}),
                                                                         number_of_examples=20, receptors_in_repertoire_count=0),
                                                           sequence_type=SequenceType.AMINO_ACID, all_signals=signals,
                                                           sequence_batch_size=100, seed=1, export_p_gens=True, keep_p_gen_dist=True,
                                                           remove_seqs_with_signals=True,
                                                           max_iterations=100, p_gen_bin_count=5))
        sequences = implanter.make_sequences(path)

        self.assertEqual(20, len(sequences))
        for sequence in sequences:
            self.assertTrue(isinstance(sequence, ReceptorSequence))
            self.assertTrue("AA" in sequence.amino_acid_sequence)
            self.assertTrue(sequence.metadata.custom_params['s1'])

        shutil.rmtree(path)
