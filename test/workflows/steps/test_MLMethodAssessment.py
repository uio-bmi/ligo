import os
import shutil
from unittest import TestCase

import numpy as np
import pandas as pd

from ligo.caching.CacheType import CacheType
from ligo.data_model.dataset.RepertoireDataset import RepertoireDataset
from ligo.data_model.encoded_data.EncodedData import EncodedData
from ligo.environment.Constants import Constants
from ligo.environment.EnvironmentSettings import EnvironmentSettings
from ligo.environment.Label import Label
from ligo.environment.LabelConfiguration import LabelConfiguration
from ligo.ml_methods.LogisticRegression import LogisticRegression
from ligo.ml_metrics.Metric import Metric
from ligo.util.PathBuilder import PathBuilder
from ligo.util.RepertoireBuilder import RepertoireBuilder
from ligo.workflows.steps.MLMethodAssessment import MLMethodAssessment
from ligo.workflows.steps.MLMethodAssessmentParams import MLMethodAssessmentParams


class TestMLMethodAssessment(TestCase):

    def setUp(self) -> None:
        os.environ[Constants.CACHE_TYPE] = CacheType.TEST.name

    def test_run(self):
        path = EnvironmentSettings.tmp_test_path / "mlmethodassessment/"
        PathBuilder.build(path)
        dataset = RepertoireDataset(repertoires=RepertoireBuilder.build(
            [["AA"], ["CC"], ["AA"], ["CC"], ["AA"], ["CC"], ["AA"], ["CC"], ["AA"], ["CC"], ["AA"], ["CC"]], path)[0])
        dataset.encoded_data = EncodedData(
            examples=np.array([[1, 1], [1, 1], [3, 3], [1, 1], [1, 1], [3, 3], [1, 1], [1, 1], [3, 3], [1, 1], [1, 1], [3, 3]]),
            labels={"l1": [1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3], "l2": [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3]}
        )

        label_config = LabelConfiguration()
        label_config.add_label("l1", [1, 3], positive_class=3)

        label = Label(name='l1', values=[1, 3], positive_class=3)

        method1 = LogisticRegression()
        method1.fit(dataset.encoded_data, label=label)

        res = MLMethodAssessment.run(MLMethodAssessmentParams(
            dataset=dataset,
            method=method1,
            metrics={Metric.ACCURACY, Metric.BALANCED_ACCURACY, Metric.F1_MACRO},
            optimization_metric=Metric.LOG_LOSS,
            predictions_path=EnvironmentSettings.tmp_test_path / "mlmethodassessment/predictions.csv",
            label=label,
            ml_score_path=EnvironmentSettings.tmp_test_path / "mlmethodassessment/ml_score.csv",
            split_index=1,
            path=EnvironmentSettings.tmp_test_path / "mlmethodassessment/"
        ))

        self.assertTrue(isinstance(res, dict))
        self.assertTrue(res[Metric.LOG_LOSS.name.lower()] <= 0.1)

        self.assertTrue(os.path.isfile(EnvironmentSettings.tmp_test_path / "mlmethodassessment/ml_score.csv"))

        df = pd.read_csv(EnvironmentSettings.tmp_test_path / "mlmethodassessment/ml_score.csv")
        self.assertEqual(df.shape[0], 1)

        df = pd.read_csv(EnvironmentSettings.tmp_test_path / "mlmethodassessment/predictions.csv")
        self.assertEqual(12, df.shape[0])

        shutil.rmtree(EnvironmentSettings.tmp_test_path / "mlmethodassessment/")
