import os
import shutil
from pathlib import Path
from unittest import TestCase

import yaml

from ligo.app.LigoApp import LigoApp
from ligo.environment.EnvironmentSettings import EnvironmentSettings
from ligo.util.PathBuilder import PathBuilder


class TestLIgOSimulation(TestCase):

    def prepare_specs(self, path) -> Path:

        with (path / 'sample_source.py').open("w") as file:
            file.write("def is_present(sequence_aa: str, sequence: str, v_call: str, j_call: str) -> bool:\n\t"
                       "return any(aa in sequence_aa for aa in ['A', 'T']) and len(sequence_aa) > 12")

        specs = {
            "definitions": {
                "signals": {
                    "signal1": {
                        "source_file": str(path / "sample_source.py"),
                        "is_present_func": "is_present"
                    }
                },
                "simulations": {
                    "sim1": {
                        "is_repertoire": True,
                        "paired": False,
                        "sequence_type": "amino_acid",
                        "simulation_strategy": "RejectionSampling",
                        "sim_items": {
                            "var1": {
                                "immune_events": {
                                  "ievent1": True,
                                  "ievent2": False,
                                },
                                "signals": {"signal1": 0.5},
                                "number_of_examples": 10,
                                "is_noise": False,
                                "seed": 100,
                                "receptors_in_repertoire_count": 6,
                                "generative_model": {
                                    "type": "OLGA",
                                    "model_path": None,
                                    "default_model_name": "humanTRB",
                                    "chain": 'beta',
                                }
                            }
                        }
                    }
                },
            },
            "instructions": {
                "inst1": {
                    "type": "LigoSim",
                    "simulation": "sim1",
                    "store_signal_in_receptors": True,
                    "sequence_batch_size": 100,
                    'max_iterations': 100,
                    "export_p_gens": False,
                    "number_of_processes": 1
                }
            },
            "output": {
                "format": "HTML"
            }
        }

        with open(path / "specs.yaml", "w") as file:
            yaml.dump(specs, file)

        return path / "specs.yaml"

    def test_custom_signal_func(self):
        path = PathBuilder.remove_old_and_build(EnvironmentSettings.tmp_test_path / "integration_custom_signal/")

        specs_path = self.prepare_specs(path)

        PathBuilder.build(path / "result/")

        app = LigoApp(specification_path=specs_path, result_path=path / "result/")
        app.run()

        self.assertTrue(os.path.isfile(path / "result/inst1/metadata.csv"))

        shutil.rmtree(path)
