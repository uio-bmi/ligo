import os
import pickle
import shutil
from unittest import TestCase

import numpy as np
from sklearn.linear_model import LogisticRegression as SklearnLogisticRegression

from ligo.caching.CacheType import CacheType
from ligo.data_model.encoded_data.EncodedData import EncodedData
from ligo.environment.Constants import Constants
from ligo.environment.EnvironmentSettings import EnvironmentSettings
from ligo.environment.Label import Label
from ligo.ml_methods.LogisticRegression import LogisticRegression
from ligo.util.PathBuilder import PathBuilder


class TestLogisticRegression(TestCase):

    def setUp(self) -> None:
        os.environ[Constants.CACHE_TYPE] = CacheType.TEST.name

    def test_fit(self):
        x = np.array([[1, 0, 0], [0, 1, 1], [1, 1, 1], [0, 1, 1]])
        y = {"test": np.array([1, 0, 2, 0])}

        lr = LogisticRegression()
        lr.fit(EncodedData(x, y), Label("test", values=[1, 2, 0]))

    def test_predict(self):
        x = np.array([[1, 0, 0, 0], [0, 1, 1, 0], [1, 1, 1, 0], [0, 1, 1, 1]])
        y = {"test1": ["a", "b", "c", "b"], "test2": ["a", "b", "c", "b"]}

        label = Label("test2", values=["c", "a", "b"])

        lr = LogisticRegression()
        lr.fit(EncodedData(x, y), label)

        test_x = np.array([[0, 1, 0, 1], [1, 1, 1, 0]])
        y = lr.predict(EncodedData(test_x), label)
        y_proba = lr.predict_proba(EncodedData(test_x), label)

        self.assertTrue(len(y["test2"]) == 2)
        self.assertTrue(y["test2"][1] in ["a", "b", "c"])
        self.assertEqual(list(y_proba.keys()), ["test2"])
        self.assertEqual(sorted(y_proba["test2"].keys()), ["a", "b", "c"])

        self.assertTrue(len(y_proba["test2"]["a"]) == 2)
        self.assertTrue(len(y_proba["test2"]["b"]) == 2)
        self.assertTrue(len(y_proba["test2"]["c"]) == 2)


    def test_fit_by_cross_validation(self):
        x = EncodedData(
            np.array([[1, 0, 0], [0, 1, 1], [1, 1, 1], [0, 1, 1], [1, 0, 0], [0, 1, 1], [1, 1, 1], [0, 1, 1]]),
            {"test1": [1, 0, 2, 0, 1, 0, 2, 0], "test2": [1, 0, 2, 0, 1, 0, 2, 0]})

        lr = LogisticRegression()
        lr.fit_by_cross_validation(x, number_of_splits=2, label=Label("test2", values=[0, 1, 2]))

    def test_store(self):
        x = np.array([[1, 0, 0], [0, 1, 1], [1, 1, 1], [0, 1, 1]])
        y = {"default": np.array([1, 0, 2, 0])}

        lr = LogisticRegression()
        lr.fit(EncodedData(x, y), Label("default", values=[0, 1, 2]))

        path = EnvironmentSettings.root_path / "test/tmp/lr/"

        lr.store(path, ["f1", "f2", "f3"])
        self.assertTrue(os.path.isfile(path / "logistic_regression.pickle"))

        with open(path / "logistic_regression.pickle", "rb") as file:
            lr2 = pickle.load(file)

        self.assertTrue(isinstance(lr2, SklearnLogisticRegression))

        shutil.rmtree(path)

    def test_load(self):
        x = np.array([[1, 0, 0], [0, 1, 1], [1, 1, 1], [0, 1, 1]])
        y = {"default": np.array([1, 0, 2, 0])}

        lr = LogisticRegression()
        lr.fit(EncodedData(x, y), Label("default", values=[1, 0, 2]))

        path = EnvironmentSettings.root_path / "test/tmp/lr2/"
        PathBuilder.build(path)

        with open(path / "logistic_regression.pickle", "wb") as file:
            pickle.dump(lr.model, file)

        lr2 = LogisticRegression()
        lr2.load(path)

        self.assertTrue(isinstance(lr2.model, SklearnLogisticRegression))

        shutil.rmtree(path)

