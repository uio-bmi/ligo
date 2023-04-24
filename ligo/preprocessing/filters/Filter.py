from abc import ABC

import pandas as pd

from ligo.data_model.dataset.Dataset import Dataset
from ligo.data_model.dataset.RepertoireDataset import RepertoireDataset
from ligo.preprocessing.Preprocessor import Preprocessor
from ligo.util.PathBuilder import PathBuilder


class Filter(Preprocessor, ABC):

    def _build_new_metadata(self, dataset: RepertoireDataset, indices_to_keep: list):
        if dataset.metadata_file:
            df = pd.read_csv(dataset.metadata_file).iloc[indices_to_keep, :]
            df.reset_index(drop=True, inplace=True)

            PathBuilder.build(self.result_path)
            path = self.result_path / f"{dataset.metadata_file.stem}_filtered.csv"
            df.to_csv(path, index=False)
        else:
            path = None
        return path

    def _remove_empty_repertoires(self, repertoires: list):
        filtered_repertoires = []
        for repertoire in repertoires:
            if len(repertoire.sequences) > 0:
                filtered_repertoires.append(repertoire)
        return filtered_repertoires

    def check_dataset_not_empty(self, processed_dataset: Dataset, location="Filter"):
        assert processed_dataset.get_example_count() > 0, f"{location}: {type(processed_dataset).__name__} ended up empty after filtering. " \
                                                          f"Please adjust filter settings."

