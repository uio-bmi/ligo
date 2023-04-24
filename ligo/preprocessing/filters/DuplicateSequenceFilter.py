import copy
from multiprocessing.pool import Pool
from pathlib import Path

import pandas as pd

from ligo.data_model.dataset.RepertoireDataset import RepertoireDataset
from ligo.data_model.receptor.receptor_sequence.Chain import Chain
from ligo.data_model.repertoire.Repertoire import Repertoire
from ligo.environment.SequenceType import SequenceType
from ligo.preprocessing.filters.CountAggregationFunction import CountAggregationFunction
from ligo.preprocessing.filters.Filter import Filter
from ligo.util.ParameterValidator import ParameterValidator
from scripts.specification_util import update_docs_per_mapping


class DuplicateSequenceFilter(Filter):
    """
    Collapses duplicate nucleotide or amino acid sequences within each repertoire in the given RepertoireDataset.
    This filter can be applied to Repertoires and RepertoireDatasets.

    Sequences are considered duplicates if the following fields are identical:

      - amino acid or nucleotide sequence (whichever is specified)
      - v and j genes (note that the full field including subgroup + gene is used for matching, i.e. V1 and V1-1 are not considered duplicates)
      - chain
      - region type

    For all other fields (the non-specified sequence type, custom lists, sequence identifier) only the first occurring
    value is kept.

    Note that this means the count value of a sequence with a given sequence identifier might not be the same as before
    removing duplicates, unless count_agg = FIRST is used.

    Arguments:

        filter_sequence_type (:py:obj:`~immuneML.environment.SequenceType.SequenceType`): Whether the sequences should be collapsed on the nucleotide or amino acid level. Valid options are defined by the SequenceType enum.

        batch_size (int): number of repertoires that can be loaded at the same time (only affects the speed)

        count_agg (:py:obj:`~immuneML.preprocessing.filters.CountAggregationFunction.CountAggregationFunction`): determines how the sequence counts of duplicate sequences are aggregated. Valid options are defined by the CountAggregationFunction enum.

    YAML specification:

    .. indent with spaces
    .. code-block:: yaml

        preprocessing_sequences:
            my_preprocessing:
                - my_filter:
                    DuplicateSequenceFilter:
                        # required parameters:
                        filter_sequence_type: AMINO_ACID
                        # optional parameters (if not specified the values bellow will be used):
                        batch_size: 4
                        count_agg: SUM

    """

    @classmethod
    def build_object(cls, **kwargs):
        location = cls.__name__
        ParameterValidator.assert_keys(kwargs.keys(), ["filter_sequence_type", "batch_size", "count_agg"], location,
                                       "DuplicateSequenceFilter")
        ParameterValidator.assert_in_valid_list(kwargs["filter_sequence_type"].upper(), [item.name for item in SequenceType],
                                                location, "filter_sequence_type")
        ParameterValidator.assert_in_valid_list(kwargs["count_agg"].upper(), [item.name for item in CountAggregationFunction], location,
                                                "count_agg")
        ParameterValidator.assert_type_and_value(kwargs["batch_size"], int, location, "batch_size", 1)
        return DuplicateSequenceFilter(filter_sequence_type=SequenceType[kwargs["filter_sequence_type"].upper()],
                                       batch_size=kwargs["batch_size"], count_agg=CountAggregationFunction[kwargs["count_agg"].upper()])

    def __init__(self, filter_sequence_type: SequenceType, batch_size: int, count_agg: CountAggregationFunction, result_path: Path = None):
        super().__init__(result_path)
        self.filter_sequence_type = filter_sequence_type
        self.count_agg = count_agg
        self.batch_size = batch_size

        self.sequence_of_interest = "sequence_aa" if filter_sequence_type == SequenceType.AMINO_ACID else "sequence"
        self.sequence_to_ignore = "sequence" if self.sequence_of_interest == "sequence_aa" else "sequence_aa"

        assert self.sequence_of_interest in Repertoire.FIELDS, f"{DuplicateSequenceFilter.__name__}: {self.sequence_of_interest} not in {Repertoire.FIELDS}"
        assert self.sequence_to_ignore in Repertoire.FIELDS, f"{DuplicateSequenceFilter.__name__}: {self.sequence_of_interest} not in {Repertoire.FIELDS}"

    def process_dataset(self, dataset: RepertoireDataset, result_path: Path, number_of_processes=1) -> RepertoireDataset:
        self.result_path = result_path if result_path is not None else self.result_path

        self.check_dataset_type(dataset, [RepertoireDataset], "DuplicateSequenceFilter")

        processed_dataset = copy.deepcopy(dataset)

        with Pool(self.batch_size) as pool:
            repertoires = pool.map(self._process_repertoire, dataset.repertoires)

        processed_dataset.repertoires = repertoires

        return processed_dataset

    def _prepare_group_by_field(self, columns):
        groupby_fields = copy.deepcopy(list(Repertoire.FIELDS))
        groupby_fields.remove(self.sequence_to_ignore)
        groupby_fields.remove("duplicate_count")
        groupby_fields.remove("sequence_id")
        groupby_fields.remove("cell_id")
        groupby_fields.remove("frame_type")

        for field in set(Repertoire.FIELDS).difference(set(columns)):
            if field in groupby_fields:
                groupby_fields.remove(field)

        return groupby_fields

    def _prepare_agg_dict(self, columns, custom_lists):

        agg_dict = {"sequence_id": "first"}

        if self.sequence_to_ignore in columns:
            agg_dict[self.sequence_to_ignore] = "first"

        if "duplicate_count" in columns:
            agg_dict["duplicate_count"] = self.count_agg.value

        if "cell_id" in columns:
            agg_dict["cell_id"] = "first"

        for key in custom_lists:
            agg_dict[key] = "first"

        return agg_dict

    def _process_repertoire(self, repertoire: Repertoire) -> Repertoire:
        data = pd.DataFrame(repertoire.load_data())

        groupby_fields = self._prepare_group_by_field(data.columns)
        custom_lists = list(set(data.columns) - set(Repertoire.FIELDS))
        agg_dict = self._prepare_agg_dict(data.columns, custom_lists)

        # Chain objects can not be aggregated, convert to strings
        if "chain" in data.columns:
            data["chain"] = [chain.value if isinstance(chain, Chain) else chain for chain in data["chain"]]
        else:
            data["chain"] = None

        no_duplicates = data.groupby(groupby_fields).agg(agg_dict).reset_index()

        processed_repertoire = Repertoire.build(sequence_aa=list(no_duplicates["sequence_aa"]) if "sequence_aa" in no_duplicates.columns else None,
                                                sequence=list(no_duplicates["sequence"]) if "sequence" in no_duplicates.columns else None,
                                                v_call=list(no_duplicates["v_call"]) if "v_call" in no_duplicates.columns else None,
                                                j_call=list(no_duplicates["j_call"]) if 'j_call' in no_duplicates.columns else None,
                                                chain=[Chain.get_chain(key) for key in
                                                        list(no_duplicates["chain"])] if "chain" in no_duplicates.columns else None,
                                                duplicate_count=list(no_duplicates["duplicate_count"]) if "duplicate_count" in no_duplicates else None,
                                                region_type=list(no_duplicates["region_type"]) if "region_type" in no_duplicates else None,
                                                custom_lists={key: list(no_duplicates[key]) for key in custom_lists},
                                                sequence_id=list(no_duplicates["sequence_id"]),
                                                metadata=copy.deepcopy(repertoire.metadata),
                                                path=self.result_path,
                                                filename_base=f"{repertoire.data_filename.stem}_filtered")

        return processed_repertoire

    @staticmethod
    def get_documentation():
        doc = str(DuplicateSequenceFilter.__doc__)

        mapping = {
            "Valid options are defined by the CountAggregationFunction enum.": f"Valid values are: {[e.name for e in CountAggregationFunction]}.",
            "Valid options are defined by the SequenceType enum.": f"Valid values are: {[e.name for e in SequenceType]}."
        }

        doc = update_docs_per_mapping(doc, mapping)

        return doc
