import logging

import airr
import pandas as pd

from ligo.IO.dataset_import.DataImport import DataImport
from ligo.IO.dataset_import.DatasetImportParams import DatasetImportParams
from ligo.data_model.dataset.Dataset import Dataset
from ligo.data_model.receptor.ChainPair import ChainPair
from ligo.data_model.receptor.RegionType import RegionType
from ligo.data_model.receptor.receptor_sequence.SequenceFrameType import SequenceFrameType
from ligo.data_model.repertoire.Repertoire import Repertoire
from ligo.util.ImportHelper import ImportHelper
from scripts.specification_util import update_docs_per_mapping


class AIRRImport(DataImport):
    """
    Imports data in AIRR format. The AIRR .tsv format is explained here: https://docs.airr-community.org/en/stable/datarep/format.html
    And the AIRR rearrangement schema can be found here: https://docs.airr-community.org/en/stable/datarep/rearrangements.html

    Arguments:

    - path (str): Either the path to the file to import, or the path to the folder locating one or multiple files with .tsv, .csv or .txt extensions. By default path is set to the current working directory.

    - is_repertoire (bool): Should be set to False, as we import a SequenceDataset. 

    - import_productive (bool): Whether productive sequences (with value 'T' in column productive) should be included in the imported sequences. By default, import_productive is True.

    - import_with_stop_codon (bool): Whether sequences with stop codons (with value 'T' in column stop_codon) should be included in the imported sequences. This only applies if column stop_codon is present. By default, import_with_stop_codon is False.

    - import_out_of_frame (bool): Whether out of frame sequences (with value 'F' in column vj_in_frame) should be included in the imported sequences. This only applies if column vj_in_frame is present. By default, import_out_of_frame is False.

    - import_illegal_characters (bool): Whether to import sequences that contain illegal characters, i.e., characters that do not appear in the sequence alphabet (amino acids including stop codon '*', or nucleotides). When set to false, filtering is only applied to the sequence type of interest (when running immuneML in amino acid mode, only entries with illegal characters in the amino acid sequence are removed). By default import_illegal_characters is False.

    - import_empty_nt_sequences (bool): imports sequences which have an empty nucleotide sequence field; can be True or False. By default, import_empty_nt_sequences is set to True.

    - import_empty_aa_sequences (bool): imports sequences which have an empty amino acid sequence field; can be True or False; for analysis on amino acid sequences, this parameter should be False (import only non-empty amino acid sequences). By default, import_empty_aa_sequences is set to False.

    - region_type (str): Which part of the sequence to import. By default, this value is set to IMGT_CDR3. This means the first and last amino acids are removed from the CDR3 sequence, as AIRR uses the IMGT junction. Specifying any other value will result in importing the sequences as they are. Valid values for region_type are the names of the :py:obj:`~immuneML.data_model.receptor.RegionType.RegionType` enum.

    - column_mapping (dict): A mapping from AIRR column names to immuneML's internal data representation. A custom column mapping can be specified here if necessary (for example; adding additional data fields if they are present in the AIRR file, or using alternative column names). Valid immuneML fields that can be specified here are defined by Repertoire.FIELDS. For AIRR, this is by default set to:

        .. indent with spaces
        .. code-block:: yaml

            junction: sequence
            junction_aa: sequence_aa
            locus: chain

    - column_mapping_synonyms (dict): This is a column mapping that can be used if a column could have alternative names. The formatting is the same as column_mapping. If some columns specified in column_mapping are not found in the file, the columns specified in column_mapping_synonyms are instead attempted to be loaded. For AIRR format, there is no default column_mapping_synonyms.

    - metadata_column_mapping (dict): Specifies metadata for Sequence- and ReceptorDatasets. This should specify a mapping similar to column_mapping where keys are AIRR column names and values are the names that are internally used in immuneML as metadata fields. These metadata fields can be used as prediction labels for Sequence- and ReceptorDatasets. This parameter can also be used to specify sequence-level metadata columns for RepertoireDatasets, which can be used by reports. To set prediction label metadata for RepertoireDatasets, see metadata_file instead. For AIRR format, there is no default metadata_column_mapping.

    - separator (str): Column separator, for AIRR this is by default "\\t".


    YAML specification:

    .. indent with spaces
    .. code-block:: yaml

        my_airr_dataset:
            format: AIRR
            params:
                path: path/to/files/
                is_repertoire: False
                import_productive: True # whether to include productive sequences in the dataset
                import_with_stop_codon: False # whether to include sequences with stop codon in the dataset
                import_out_of_frame: False # whether to include out of frame sequences in the dataset
                import_illegal_characters: False # remove sequences with illegal characters for the sequence_type being used
                import_empty_nt_sequences: True # keep sequences even if the `sequences` column is empty (provided that other fields are as specified here)
                import_empty_aa_sequences: False # remove all sequences with empty `sequence_aa` column
                # Optional fields with AIRR-specific defaults, only change when different behavior is required:
                separator: "\\t" # column separator
                region_type: IMGT_CDR3 # what part of the sequence to import
                column_mapping: # column mapping AIRR: immuneML
                    junction: sequence
                    junction_aa: sequence_aa
                    locus: chain

    """

    @staticmethod
    def import_dataset(params: dict, dataset_name: str) -> Dataset:
        return ImportHelper.import_dataset(AIRRImport, params, dataset_name)

    @staticmethod
    def preprocess_dataframe(df: pd.DataFrame, params: DatasetImportParams):
        """
        Function for preprocessing data from a dataframe containing AIRR data, such that:
            - productive sequences, sequences with stop codons or out of frame sequences are filtered according to specification
            - if RegionType is CDR3, the leading C and trailing W are removed from the sequence to match the CDR3 definition
            - if no chain column was specified, the chain is extracted from the v gene name
            - the allele information is removed from the V and J genes
        """
        if "productive" in df.columns:
            df["frame_type"] = SequenceFrameType.OUT.name
            df.loc[df["productive"], "frame_type"] = SequenceFrameType.IN.name
        else:
            df["frame_type"] = None

        if "vj_in_frame" in df.columns:
            df.loc[df["vj_in_frame"] == 'T', "frame_type"] = SequenceFrameType.IN.name
        if "stop_codon" in df.columns:
            df.loc[df["stop_codon"] == 'T', "frame_type"] = SequenceFrameType.STOP.name

        if "productive" in df.columns:
            frame_type_list = ImportHelper.prepare_frame_type_list(params)
            df = df[df["frame_type"].isin(frame_type_list)]

        if params.region_type == RegionType.IMGT_CDR3:
            if 'sequence' in df.columns:
                df.drop(['sequence'], axis=1, inplace=True)
            if "cdr3" in df.columns or "cdr3_aa" in df.columns:
                df.rename(columns={"cdr3": "sequence", "cdr3_aa": "sequence_aa"}, inplace=True)
            elif "junction" in df.columns or "junction_aa" in df.columns:
                df.rename(columns={'junction': 'sequence', 'junction_aa': 'sequence_aa'}, inplace=True)
                ImportHelper.junction_to_cdr3(df, params.region_type)

        df.loc[:, "region_type"] = params.region_type.name

        ImportHelper.drop_empty_sequences(df, params.import_empty_aa_sequences, params.import_empty_nt_sequences)
        ImportHelper.drop_illegal_character_sequences(df, params.import_illegal_characters, import_with_stop_codon=params.import_with_stop_codon)
        ImportHelper.load_chains(df)

        return df

    @staticmethod
    def alternative_load_func(filename, params: DatasetImportParams):
        try:
            df = airr.load_rearrangement(filename)
        except Exception as e:
            logging.warning(f"Could not load file {filename} with airr.load_rearrangement. Trying to load with pandas.")
            df = pd.read_csv(filename, sep=params.separator).dropna(axis=1, how='all').dropna(axis=0, how='all')
            if 'productive' in df.columns:
                df['productive'] = df['productive'] == 'T'

        ImportHelper.standardize_none_values(df)
        df.dropna(axis="columns", how="all", inplace=True)
        return df

    @staticmethod
    def import_receptors(df, params):
        df["receptor_id"] = df["cell_id"]
        return ImportHelper.import_receptors(df, params)

    @staticmethod
    def get_documentation():
        doc = str(AIRRImport.__doc__)

        chain_pair_values = str([chain_pair.name for chain_pair in ChainPair])[1:-1].replace("'", "`")
        region_type_values = str([region_type.name for region_type in RegionType])[1:-1].replace("'", "`")
        repertoire_fields = list(Repertoire.FIELDS)
        repertoire_fields.remove("region_type")

        mapping = {
            "Valid values for receptor_chains are the names of the :py:obj:`~immuneML.data_model.receptor.ChainPair.ChainPair` enum.": f"Valid values are {chain_pair_values}.",
            "Valid values for region_type are the names of the :py:obj:`~immuneML.data_model.receptor.RegionType.RegionType` enum.": f"Valid values are {region_type_values}.",
            "Valid immuneML fields that can be specified here are defined by Repertoire.FIELDS": f"Valid immuneML fields that can be specified here are {repertoire_fields}."
        }
        doc = update_docs_per_mapping(doc, mapping)
        return doc
