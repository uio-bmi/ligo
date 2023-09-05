import math
import numpy as np

from ligo.data_model.receptor.RegionType import RegionType
from ligo.data_model.receptor.receptor_sequence.ReceptorSequence import ReceptorSequence
from ligo.environment.SequenceType import SequenceType


class PositionHelper:

    @staticmethod
    def get_imgt_position_weights_for_annotation(input_length: int, region_type: RegionType,
                                                 sequence_position_weights: dict):
        imgt_positions = PositionHelper.gen_imgt_positions_from_length(input_length, region_type)

        position_weights = {}
        for index, position in enumerate(imgt_positions):
            if position in sequence_position_weights:
                position_weights[position] = sequence_position_weights[position]

        weights_sum = sum(list(position_weights.values()))
        remaining_weight_for_position = (1 - weights_sum) / (len(imgt_positions) - len(position_weights))
        for position in imgt_positions:
            if position not in position_weights:
                position_weights[position] = remaining_weight_for_position

        assert np.isclose(sum(list(position_weights.values())), 1), position_weights

        return {position: position_weights[position] for position in imgt_positions}

    @staticmethod
    def get_allowed_positions_for_annotation(input_length: int, region_type: RegionType, sequence_position_weights: dict):
        position_weights = PositionHelper.get_imgt_position_weights_for_annotation(input_length, region_type,
                                                                                   sequence_position_weights)
        return [int(bool(weight)) for weight in position_weights.values()]

    @staticmethod
    def get_imgt_position_weights_for_implanting(input_length: int, region_type: RegionType,
                                                 sequence_position_weights: dict, limit: int):
        position_weights = PositionHelper.get_imgt_position_weights_for_annotation(input_length, region_type, sequence_position_weights)

        for index, position in enumerate(position_weights.keys()):
            if index > input_length - limit:
                position_weights[position] = 0.

        weights_sum = sum(list(position_weights.values()))
        return {position: weight / weights_sum for position, weight in position_weights.items()}

    @staticmethod
    def gen_imgt_positions_from_cdr3_length(input_length: int):
        start = 105
        end = 117
        imgt_range = list(range(start, end + 1))
        length = input_length if input_length < 14 else 13
        imgt_positions = imgt_range[:math.ceil(length / 2)] + imgt_range[-math.floor(length / 2):]
        if input_length > 13:
            len_insert = input_length - 13
            insert_left = [111 + 0.1 * i for i in range(1, math.floor(len_insert / 2) + 1)]
            insert_right = [112 + 0.1 * i for i in range(1, math.ceil(len_insert / 2) + 1)]
            insert = insert_left + list(reversed(insert_right))
            imgt_positions[math.ceil(len(imgt_range) / 2):math.ceil(len(imgt_range) / 2)] = insert
        return imgt_positions

    @staticmethod
    def gen_imgt_positions_from_junction_length(input_length: int):
        return [104] + PositionHelper.gen_imgt_positions_from_cdr3_length(input_length - 2) + [118]

    @staticmethod
    def gen_imgt_positions_from_sequence(sequence: ReceptorSequence,
                                         sequence_type: SequenceType = SequenceType.AMINO_ACID):
        if sequence_type != SequenceType.AMINO_ACID:
            raise NotImplementedError(f"{sequence_type.name} is currently not supported for obtaining IMGT positions")
        region_type = sequence.get_attribute("region_type")
        input_length = len(sequence.get_sequence(sequence_type=sequence_type))

        return PositionHelper.gen_imgt_positions_from_length(input_length, region_type)

    @staticmethod
    def gen_imgt_positions_from_length(input_length: int, region_type: RegionType):
        if region_type == RegionType.IMGT_CDR3:
            return PositionHelper.gen_imgt_positions_from_cdr3_length(input_length)
        if region_type == RegionType.IMGT_JUNCTION:
            return PositionHelper.gen_imgt_positions_from_junction_length(input_length)
        else:
            raise NotImplementedError(
                f"PositionHelper: IMGT positions are not implemented for region type {region_type}")
