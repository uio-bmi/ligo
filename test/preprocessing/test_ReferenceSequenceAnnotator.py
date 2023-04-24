import shutil
from pathlib import Path

from ligo.data_model.receptor.receptor_sequence.ReceptorSequence import ReceptorSequence
from ligo.data_model.receptor.receptor_sequence.SequenceMetadata import SequenceMetadata
from ligo.environment.EnvironmentSettings import EnvironmentSettings
from ligo.preprocessing.ReferenceSequenceAnnotator import ReferenceSequenceAnnotator
from ligo.simulation.dataset_generation.RandomDatasetGenerator import RandomDatasetGenerator
from ligo.util.PathBuilder import PathBuilder


def test_process_dataset():
    compairr_paths = [Path("/usr/local/bin/compairr"), Path("./compairr/src/compairr")]

    for compairr_path in compairr_paths:
        if compairr_path.exists():
            run_test(compairr_path)
            break


def run_test(compairr_path):

    path = PathBuilder.remove_old_and_build(EnvironmentSettings.tmp_test_path / 'ref_seq_annotator')

    annotator = ReferenceSequenceAnnotator([ReceptorSequence("AAA", metadata=SequenceMetadata(region_type='FULL_SEQUENCE')),
                                            ReceptorSequence("AAC", metadata=SequenceMetadata(region_type='FULL_SEQUENCE')),
                                            ReceptorSequence("AAT", metadata=SequenceMetadata(region_type='FULL_SEQUENCE')),
                                            ReceptorSequence("AAD", metadata=SequenceMetadata(region_type='FULL_SEQUENCE'))],
                                           0, compairr_path, ignore_genes=True, threads=4, output_column_name='match_test')

    dataset = RandomDatasetGenerator.generate_repertoire_dataset(5, {500: 1.}, {3: 1}, {}, path / 'input_dataset')

    annotated_dataset = annotator.process_dataset(dataset, path / 'result', 4)

    for repertoire in annotated_dataset.repertoires:
        annotations = repertoire.get_attribute('match_test')
        assert annotations is not None
        assert annotations.dtype == int

    shutil.rmtree(path)
