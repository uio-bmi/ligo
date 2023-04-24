import os
import shutil
from unittest import TestCase

from ligo.analysis.data_manipulation.NormalizationType import NormalizationType
from ligo.caching.CacheType import CacheType
from ligo.encodings.kmer_frequency.KmerFrequencyEncoder import KmerFrequencyEncoder
from ligo.util.ReadsType import ReadsType
from ligo.encodings.kmer_frequency.sequence_encoding.SequenceEncodingType import SequenceEncodingType
from ligo.environment.Constants import Constants
from ligo.environment.EnvironmentSettings import EnvironmentSettings
from ligo.environment.LabelConfiguration import LabelConfiguration
from ligo.environment.SequenceType import SequenceType
from ligo.hyperparameter_optimization.HPSetting import HPSetting
from ligo.hyperparameter_optimization.config.ReportConfig import ReportConfig
from ligo.hyperparameter_optimization.config.SplitConfig import SplitConfig
from ligo.hyperparameter_optimization.config.SplitType import SplitType
from ligo.hyperparameter_optimization.strategy.GridSearch import GridSearch
from ligo.ml_methods.LogisticRegression import LogisticRegression
from ligo.ml_metrics.Metric import Metric
from ligo.simulation.dataset_generation.RandomDatasetGenerator import RandomDatasetGenerator
from ligo.workflows.instructions.TrainMLModelInstruction import TrainMLModelInstruction


class TestSequenceClassification(TestCase):

    def setUp(self) -> None:
        os.environ[Constants.CACHE_TYPE] = CacheType.TEST.name

    def test(self):

        path = EnvironmentSettings.tmp_test_path / "integration_sequence_classification/"
        dataset = RandomDatasetGenerator.generate_sequence_dataset(50, {4: 1}, {'l1': {1: 0.5, 2: 0.5}}, path / 'data')

        os.environ["cache_type"] = "test"
        encoder_params = {
            "normalization_type": NormalizationType.RELATIVE_FREQUENCY.name,
            "reads": ReadsType.UNIQUE.name,
            "sequence_encoding": SequenceEncodingType.CONTINUOUS_KMER.name,
            "sequence_type": SequenceType.AMINO_ACID.name,
            "k": 3
        }

        hp_setting = HPSetting(encoder=KmerFrequencyEncoder.build_object(dataset, **encoder_params), encoder_params=encoder_params,
                               ml_method=LogisticRegression(), ml_params={"model_selection_cv": False, "model_selection_n_folds": -1},
                               preproc_sequence=[])

        lc = LabelConfiguration()
        lc.add_label("l1", [1, 2])

        instruction = TrainMLModelInstruction(dataset, GridSearch([hp_setting]), [hp_setting],
                                              SplitConfig(SplitType.RANDOM, 1, 0.5, reports=ReportConfig()),
                                              SplitConfig(SplitType.RANDOM, 1, 0.5, reports=ReportConfig()),
                                              {Metric.BALANCED_ACCURACY}, Metric.BALANCED_ACCURACY, lc, path)

        result = instruction.run(result_path=path)

        shutil.rmtree(path)
