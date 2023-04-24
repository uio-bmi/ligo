import os
import shutil
from unittest import TestCase

from ligo.caching.CacheType import CacheType
from ligo.data_model.dataset.RepertoireDataset import RepertoireDataset
from ligo.environment.Constants import Constants
from ligo.environment.EnvironmentSettings import EnvironmentSettings
from ligo.preprocessing.filters.CountPerSequenceFilter import CountPerSequenceFilter
from ligo.util.PathBuilder import PathBuilder
from ligo.util.RepertoireBuilder import RepertoireBuilder


class TestCountPerSequenceFilter(TestCase):

    def setUp(self) -> None:
        os.environ[Constants.CACHE_TYPE] = CacheType.TEST.name

    def test_process(self):
        path = EnvironmentSettings.root_path / "test/tmp/count_per_seq_filter/"
        PathBuilder.build(path)
        dataset = RepertoireDataset(repertoires=RepertoireBuilder.build([["ACF", "ACF", "ACF"],
                                                                         ["ACF", "ACF"],
                                                                         ["ACF", "ACF", "ACF", "ACF"]], path,
                                                                        seq_metadata=[[{"duplicate_count": 1}, {"duplicate_count": 2},
                                                                                       {"duplicate_count": 3}], [{"duplicate_count": 4},
                                                                                                                 {"duplicate_count": 1}],
                                                                                      [{"duplicate_count": 5}, {"duplicate_count": 6},
                                                                                       {"duplicate_count": None},
                                                                                       {"duplicate_count": 1}]])[0])

        dataset1 = CountPerSequenceFilter(**{"low_count_limit": 2, "remove_without_count": True, "remove_empty_repertoires": False,
                                             "result_path": path, "batch_size": 4}).process_dataset(dataset, path)
        self.assertEqual(2, dataset1.repertoires[0].get_sequence_aas().shape[0])

        dataset2 = CountPerSequenceFilter(**{"low_count_limit": 5, "remove_without_count": True, "remove_empty_repertoires": False,
                                             "result_path": path, "batch_size": 4}).process_dataset(dataset, path)
        self.assertEqual(0, dataset2.repertoires[0].get_sequence_aas().shape[0])

        dataset3 = CountPerSequenceFilter(**{"low_count_limit": 0, "remove_without_count": True, "remove_empty_repertoires": False,
                                             "result_path": path, "batch_size": 4}).process_dataset(dataset, path)
        self.assertEqual(3, dataset3.repertoires[2].get_sequence_aas().shape[0])

        dataset = RepertoireDataset(repertoires=RepertoireBuilder.build([["ACF", "ACF", "ACF"],
                                                                         ["ACF", "ACF"],
                                                                         ["ACF", "ACF", "ACF", "ACF"]], path,
                                                                        seq_metadata=[[{"duplicate_count": None}, {"duplicate_count": None},
                                                                                       {"duplicate_count": None}],
                                                                                      [{"duplicate_count": None}, {"duplicate_count": None}],
                                                                                      [{"duplicate_count": None}, {"duplicate_count": None},
                                                                                       {"duplicate_count": None}, {"duplicate_count": None}]])[0])

        dataset4 = CountPerSequenceFilter(**{"low_count_limit": 0, "remove_without_count": True, "remove_empty_repertoires": False,
                                             "result_path": path, "batch_size": 4}).process_dataset(dataset, path)
        self.assertEqual(0, dataset4.repertoires[0].get_sequence_aas().shape[0])
        self.assertEqual(0, dataset4.repertoires[1].get_sequence_aas().shape[0])
        self.assertEqual(0, dataset4.repertoires[2].get_sequence_aas().shape[0])

        self.assertRaises(AssertionError, CountPerSequenceFilter(**{"low_count_limit": 10, "remove_without_count": True,
                                                                    "remove_empty_repertoires": True, "result_path": path,
                                                                    "batch_size": 4}).process_dataset, dataset, path)

        shutil.rmtree(path)
