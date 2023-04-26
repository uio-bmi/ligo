# quality: gold
import os
from pathlib import Path

from ligo.environment.Constants import Constants
from ligo.environment.SequenceType import SequenceType
from ligo.util.Logger import print_log
from ligo.util.PathBuilder import PathBuilder


class EnvironmentSettings:
    """
    Class containing environment variables, like receptor_sequence type,
    root path etc.
    """

    sequence_type = SequenceType.AMINO_ACID
    root_path = Path(os.path.normpath(os.path.dirname(os.path.abspath(__file__)) + "/../../") + "/")
    default_params_path = root_path / "ligo/config/default_params"
    tmp_test_path = root_path / "test/tmp"
    default_analysis_path = root_path / "analysis_runs"
    cache_path = root_path / "cache"
    tmp_cache_path = tmp_test_path / "cache"
    html_templates_path = root_path / "ligo/presentation/html/templates"
    specs_docs_path = root_path / "docs_source/specs"
    source_docs_path = root_path / "docs_source"
    max_sequence_length = 20
    low_memory = True

    @staticmethod
    def reset_cache_path():
        EnvironmentSettings.cache_path = EnvironmentSettings.root_path / "cache"
        del os.environ[Constants.CACHE_PATH]

    @staticmethod
    def set_cache_path(path: Path):
        EnvironmentSettings.cache_path = Path(path)
        PathBuilder.build(path)
        os.environ[Constants.CACHE_PATH] = str(EnvironmentSettings.cache_path)
        print_log(f"Setting temporary cache path to {path}", include_datetime=True)

    @staticmethod
    def set_sequence_type(sequence_type: SequenceType):
        EnvironmentSettings.sequence_type = sequence_type

    @staticmethod
    def get_sequence_type() -> SequenceType:
        return EnvironmentSettings.sequence_type

    @staticmethod
    def get_sequence_alphabet(sequence_type: SequenceType = None):
        """
        :return: alphabetically sorted receptor_sequence alphabet
        """
        seq_type = sequence_type if sequence_type is not None else EnvironmentSettings.sequence_type
        if seq_type == SequenceType.AMINO_ACID:
            alphabet = list("ACDEFGHIKLMNPQRSTVWY")
            alphabet.sort()
        elif seq_type == SequenceType.NUCLEOTIDE:
            alphabet = list("ACGT")
            alphabet.sort()
        else:
            raise RuntimeError("EnvironmentSettings: the sequence alphabet cannot be obtained if sequence_type was not set properly. "
                               f"Expected AMINO_ACID or NUCLEOTIDE, but got {seq_type} instead.")
        return alphabet
