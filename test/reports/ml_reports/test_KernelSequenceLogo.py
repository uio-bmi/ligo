import os
import shutil
from unittest import TestCase

from ligo.caching.CacheType import CacheType
from ligo.encodings.EncoderParams import EncoderParams
from ligo.encodings.onehot.OneHotReceptorEncoder import OneHotReceptorEncoder
from ligo.environment.Constants import Constants
from ligo.environment.EnvironmentSettings import EnvironmentSettings
from ligo.environment.Label import Label
from ligo.environment.LabelConfiguration import LabelConfiguration
from ligo.ml_methods.ReceptorCNN import ReceptorCNN
from ligo.reports.ml_reports.KernelSequenceLogo import KernelSequenceLogo
from ligo.simulation.dataset_generation.RandomDatasetGenerator import RandomDatasetGenerator
from ligo.util.PathBuilder import PathBuilder


class TestKernelSequenceLogo(TestCase):

    def setUp(self) -> None:
        os.environ[Constants.CACHE_TYPE] = CacheType.TEST.name

    def test_generate(self):
        path = PathBuilder.build(EnvironmentSettings.tmp_test_path / "kernel_sequence_logo/")
        dataset = RandomDatasetGenerator.generate_receptor_dataset(receptor_count=500, chain_1_length_probabilities={4: 1},
                                                                   chain_2_length_probabilities={4: 1},
                                                                   labels={"CMV": {True: 0.5, False: 0.5}}, path=path / "dataset")
        enc_dataset = OneHotReceptorEncoder(True, 1, False, "enc1").encode(dataset, EncoderParams(path / "result",
                                                                                                  LabelConfiguration([Label("CMV", [True, False])])))
        cnn = ReceptorCNN(kernel_count=2, kernel_size=[3], positional_channels=3, sequence_type="amino_acid", device="cpu",
                          number_of_threads=4, random_seed=1, learning_rate=0.01, iteration_count=10, l1_weight_decay=0.1, evaluate_at=5,
                          batch_size=100, training_percentage=0.8, l2_weight_decay=0.0)
        cnn.fit(enc_dataset.encoded_data, Label("CMV", [True, False]))

        report = KernelSequenceLogo(method=cnn, result_path=path / "logos/")
        report.generate_report()

        self.assertTrue(os.path.isfile(path / "logos/alpha_kernel_3_1.png"))
        self.assertTrue(os.path.isfile(path / "logos/alpha_kernel_3_2.png"))
        self.assertTrue(os.path.isfile(path / "logos/beta_kernel_3_1.png"))
        self.assertTrue(os.path.isfile(path / "logos/beta_kernel_3_2.png"))
        self.assertTrue(os.path.isfile(path / "logos/alpha_kernel_3_1.csv"))
        self.assertTrue(os.path.isfile(path / "logos/alpha_kernel_3_2.csv"))
        self.assertTrue(os.path.isfile(path / "logos/beta_kernel_3_1.csv"))
        self.assertTrue(os.path.isfile(path / "logos/beta_kernel_3_2.csv"))
        self.assertTrue(os.path.isfile(path / "logos/fully_connected_layer_weights.csv"))
        self.assertTrue(os.path.isfile(path / "logos/fully_connected_layer_weights.html"))

        shutil.rmtree(path)
