import os
import shutil
from glob import glob
from unittest import TestCase

from ligo.environment.EnvironmentSettings import EnvironmentSettings
from ligo.util.PathBuilder import PathBuilder
from ligo.workflows.instructions.quickstart import Quickstart


class TestQuickstart(TestCase):
    def test(self):
        path = EnvironmentSettings.tmp_test_path / "quickstart_test/"
        PathBuilder.remove_old_and_build(path)

        quickstart = Quickstart()
        quickstart.run(path)

        self.assertTrue(os.path.isfile(path / "machine_learning_analysis/result/full_specs.yaml"))
        self.assertEqual(4, len(glob(str(path / "machine_learning_analysis/result/machine_learning_instruction/split_1/**/test_predictions.csv"), recursive=True)))
        self.assertTrue(os.path.isfile(glob(str(path / "machine_learning_analysis/result/machine_learning_instruction/split_1/**/test_predictions.csv"), recursive=True)[0]))

        shutil.rmtree(path, ignore_errors=True)
