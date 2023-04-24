from ligo.data_model.receptor.receptor_sequence.ReceptorSequence import ReceptorSequence
from ligo.encodings.EncoderParams import EncoderParams
from ligo.encodings.kmer_frequency.sequence_encoding.SequenceEncodingStrategy import SequenceEncodingStrategy
from ligo.environment.Constants import Constants
from ligo.environment.EnvironmentSettings import EnvironmentSettings


class IdentitySequenceEncoder(SequenceEncodingStrategy):

    @staticmethod
    def encode_sequence(sequence: ReceptorSequence, params: EncoderParams):
        """
        Encodes a ReceptorSequence based on information from within the ReceptorSequence and SequenceMetadata
        instances. This allows for looking at frequency for whole sequences, with flexible definition of what a unique
        whole sequence is.
        :param sequence: ReceptorSequence
        :param params: EncoderParams (params["model"]["sequence"] and params["model"]["metadata_fields_to_include"] are
                        used)
        :return: list with only single feature
        """

        res = []
        sequence_type = params.model.get('sequence_type', EnvironmentSettings.sequence_type)
        if params.model.get("sequence", True):
            res.append(sequence.get_sequence(sequence_type))

        for field in params.model.get("metadata_fields_to_include", []):
            if sequence.metadata is None:
                res.append("unknown")
            else:
                res.append(getattr(sequence.metadata, field))

        return [Constants.FEATURE_DELIMITER.join(res)]

    @staticmethod
    def get_feature_names(params: EncoderParams):
        res = []
        if params.model.get("sequence", True):
            res.append("sequence")
        for field in params.model.get("metadata_fields_to_include", []):
            res.append(field)
        return res
