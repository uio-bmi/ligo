import numpy as np

from ligo.data_model.receptor.RegionType import RegionType
from ligo.util.PositionHelper import PositionHelper


def test_build_position_weights():

    for pos_weights in [None, {}]:
        imgt_positions = [104, 105, 106, 107, 108, 109, 110, 111, 111.1, 112.2, 112.1, 112, 113, 114, 115, 116, 117, 118]
        weights = PositionHelper.build_position_weights(sequence_position_weights=pos_weights,
                                                        imgt_positions=imgt_positions, limit=3)

        assert weights[118] == 0 and weights[117] == 0, (weights[117], weights[118])

    weights = PositionHelper.build_position_weights(sequence_position_weights={107: 0.5, 109: 0.2},
                                                    imgt_positions=imgt_positions, limit=3)

    print(weights)


def test_compute_pos_weights_from_length():
    weights = PositionHelper.compute_pos_weights_from_length(7, RegionType.IMGT_JUNCTION,
                                                             {104: 0, 105: 0}, 2)

    assert np.isclose(sum(list(weights.values())), 1), weights
    assert all(weights[pos] == 0 for pos in [104, 105, 117, 118])
    assert all(np.isclose(weights[pos], 0.3333333333333333) for pos in [106, 107, 116])
