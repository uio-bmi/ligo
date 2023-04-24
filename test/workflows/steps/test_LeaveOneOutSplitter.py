import shutil
from unittest import TestCase

from ligo.data_model.dataset.ReceptorDataset import ReceptorDataset
from ligo.data_model.receptor.TCABReceptor import TCABReceptor
from ligo.data_model.receptor.receptor_sequence.ReceptorSequence import ReceptorSequence
from ligo.environment.EnvironmentSettings import EnvironmentSettings
from ligo.hyperparameter_optimization.config.LeaveOneOutConfig import LeaveOneOutConfig
from ligo.hyperparameter_optimization.config.SplitConfig import SplitConfig
from ligo.hyperparameter_optimization.config.SplitType import SplitType
from ligo.util.PathBuilder import PathBuilder
from ligo.workflows.steps.data_splitter.DataSplitterParams import DataSplitterParams
from ligo.workflows.steps.data_splitter.LeaveOneOutSplitter import LeaveOneOutSplitter


class TestLeaveOneOutSplitter(TestCase):
    def test_split_dataset(self):
        path = PathBuilder.build(EnvironmentSettings.tmp_test_path / "leave_one_out_splitter/")
        receptors = []
        for i in range(10):
            receptors.append(TCABReceptor(ReceptorSequence(), ReceptorSequence(), {"subject": i % 3}))

        dataset = ReceptorDataset.build_from_objects(receptors, 100, path, 'd1')

        params = DataSplitterParams(dataset, SplitType.LEAVE_ONE_OUT_STRATIFICATION, 3, paths=[path / f"result_{i}/" for i in range(1, 4)],
                                    split_config=SplitConfig(SplitType.LEAVE_ONE_OUT_STRATIFICATION, split_count=3,
                                                             leave_one_out_config=LeaveOneOutConfig("subject", 1)))
        train_datasets, test_datasets = LeaveOneOutSplitter.split_dataset(params)

        self.assertEqual(3, len(train_datasets))
        self.assertEqual(3, len(test_datasets))

        for i in range(3):
            self.assertTrue(all(receptor.metadata["subject"] == i for receptor in test_datasets[i].get_data()))
            self.assertTrue(all(receptor.metadata["subject"] != i for receptor in train_datasets[i].get_data()))

        shutil.rmtree(path)

