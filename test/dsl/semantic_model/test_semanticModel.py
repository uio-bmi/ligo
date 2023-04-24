import os
import shutil
from unittest import TestCase

from ligo.caching.CacheType import CacheType
from ligo.data_model.dataset.RepertoireDataset import RepertoireDataset
from ligo.dsl.semantic_model.SemanticModel import SemanticModel
from ligo.encodings.word2vec.Word2VecEncoder import Word2VecEncoder
from ligo.encodings.word2vec.model_creator.ModelType import ModelType
from ligo.environment.Constants import Constants
from ligo.environment.EnvironmentSettings import EnvironmentSettings
from ligo.environment.LabelConfiguration import LabelConfiguration
from ligo.hyperparameter_optimization.HPSetting import HPSetting
from ligo.hyperparameter_optimization.config.ReportConfig import ReportConfig
from ligo.hyperparameter_optimization.config.SplitConfig import SplitConfig
from ligo.hyperparameter_optimization.config.SplitType import SplitType
from ligo.hyperparameter_optimization.strategy.GridSearch import GridSearch
from ligo.ml_methods.LogisticRegression import LogisticRegression
from ligo.ml_metrics.Metric import Metric
from ligo.util.PathBuilder import PathBuilder
from ligo.util.RepertoireBuilder import RepertoireBuilder
from ligo.workflows.instructions.TrainMLModelInstruction import TrainMLModelInstruction


class TestSemanticModel(TestCase):

    def setUp(self) -> None:
        os.environ[Constants.CACHE_TYPE] = CacheType.TEST.name

    def test_run(self):

        path = EnvironmentSettings.root_path / "test/tmp/smmodel/"
        PathBuilder.build(path)
        repertoires, metadata = RepertoireBuilder.build([["AAA", "CCC"], ["TTTT"], ["AAA", "CCC"], ["TTTT"],
                                                       ["AAA", "CCC"], ["TTTT"], ["AAA", "CCC"], ["TTTT"],
                                                       ["AAA", "CCC"], ["TTTT"], ["AAA", "CCC"], ["TTTT"],
                                                       ["AAA", "CCC"], ["TTTT"], ["AAA", "CCC"], ["TTTT"],
                                                       ["AAA", "CCC"], ["TTTT"], ["AAA", "CCC"], ["TTTT"],
                                                       ["AAA", "CCC"], ["TTTT"], ["AAA", "CCC"], ["TTTT"],
                                                       ["AAA", "CCC"], ["TTTT"], ["AAA", "CCC"], ["TTTT"],
                                                       ["AAA", "CCC"], ["TTTT"], ["AAA", "CCC"], ["TTTT"]], path,
                                                      {"default": [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2,
                                                                   1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2]})
        dataset = RepertoireDataset(repertoires=repertoires,
                                    labels={"default": [1, 2]},
                                    metadata_file=metadata)

        label_config = LabelConfiguration()
        label_config.add_label("default", [1, 2])

        encoder_params = {"vector_size": 8, "model_type": ModelType.SEQUENCE.name, "k": 3, "epochs": 10, "window": 5}
        hp_settings = [HPSetting(Word2VecEncoder.build_object(dataset, **encoder_params), encoder_params, LogisticRegression(),
                                 {"model_selection_cv": False, "model_selection_n_folds": -1}, [])]

        split_config_assessment = SplitConfig(SplitType.RANDOM, 1, 0.5, ReportConfig())
        split_config_selection = SplitConfig(SplitType.RANDOM, 1, 0.5, ReportConfig())

        instruction = TrainMLModelInstruction(dataset, GridSearch(hp_settings), hp_settings,
                                              split_config_assessment,
                                              split_config_selection,
                                              {Metric.BALANCED_ACCURACY}, Metric.BALANCED_ACCURACY,
                                              label_config, path)
        semantic_model = SemanticModel([instruction], path)

        semantic_model.run()

        shutil.rmtree(path)
