
import json
import numpy as np
import pytest
from beta_move.beta_move import BetaMove
from beta_move.climb import Climb
from beta_move.moonboard import Moonboard


x_342797 = np.array([
        [5., 4., 9., 4., 1., 1., 5., 4., 1., 0.],
        [0., 2., 4., 2., 0., 0., 4., 7., 0., 0.],
        [1., 5., 2., 0., 0., 0., 0., 8., 0., 0.],
        [0., 0., 4., 9., 4., 0., 7., 9., 0., 0.],
        [0., 0., 6., 4., 4., 0., 3., 11., 0., 0.],
        [0., 3., 6., 3., 0., 0., 4., 12., 0., 0.],
        [1., 4., 3., 1., 0., 0., 2., 14., 0., 0.],
        [2., 5., 2., 1., 0., 0., 1., 15., 0., 0.],
        [2., 6., 8., 6., 2., 0., 3., 17., 0., 1.]
    ])


def setup_standard() -> Moonboard:
    board = Moonboard(2016)
    app = BetaMove(board)
    f = open('tests/Unit/342797.json')
    data = json.load(f)
    climb = Climb.from_json("342797", data["342797"])
    app.create_movement(climb)
    return app


def test_constructor() -> None:
    board = Moonboard(2016)
    app = BetaMove(board)
    assert isinstance(app, BetaMove)


def test_match_hold_features() -> None:
    expected = x_342797.T
    board = Moonboard(2016)
    app = BetaMove(board)
    f = open('tests/Unit/342797.json')
    data = json.load(f)
    climb = Climb.from_json("342797", data["342797"])
    np.testing.assert_array_equal(app.match_hold_features(climb), expected)


def test_create_movement() -> None:
    expected = {
        "hold_index": [0, 0, 1, 3, 4, 5, 7, 8],
        "hands": ['LH', 'RH', 'LH', 'RH', 'LH', 'RH', 'LH', 'RH'],
        "success": 98.50396893
    }
    board = Moonboard(2016)
    app = BetaMove(board)
    f = open('tests/Unit/342797.json')
    data = json.load(f)
    climb = Climb.from_json("342797", data["342797"])
    result = app.create_movement(climb)
    assert result.handSequence == expected["hold_index"]
    assert result.handOperator == expected["hands"]
    assert result.overall_success_rate() == expected["sucess"]


def test_success_by_hold() -> None:
    app = setup_standard()
    hold = app.allHolds[0]
    assert app.success_rate_by_hold(hold, "LH") == 8
    assert app.success_rate_by_hold(hold, "RH") == 7


def test_add_start() -> None:
    app = BetaMove(Moonboard())
    app.allHolds = x_342797
    app.totalNumOfHold = np.size(app.allHolds, axis=1)
    app.holdsNotUsed = list(range(app.totalNumOfHold))
    app.add_start_holds(False)
    assert app.handSequence == [0, 0]
    assert app.handOperator == ["LH", "RH"]


last_move_success_data = [
    [[list(range(1, 8)), [0, 0], ['LH', 'RH']], 56]
]


@pytest.mark.parametrize("input, expected", last_move_success_data)
def test_last_move_success(input, expected: int) -> None:
    board = Moonboard(2016)
    app = BetaMove(board)
    app.allHolds = x_342797
    app.totalNumOfHold = np.size(app.allHolds, axis=1)
    app.holdsNotUsed = input[0]
    app.handSequence = input[1]
    app.handOperator = input[2]
    result = app.last_move_success_rate_by_hold()
    assert result == expected


def test_overall_success() -> None:
    app = setup_standard()
    app.handSequence = [0, 0, 1, 3, 4, 5, 7, 8]
    app.handOperator = ['LH', 'RH', 'LH', 'RH', 'LH', 'RH', 'LH', 'RH']
    assert app.overall_success_rate() == 98.503968934466


def test_get_all() -> None:
    expected = x_342797
    app = setup_standard()
    np.testing.assert_array_equal(app.get_all_holds(), expected)


def test_get_left_hand_order() -> None:
    app = BetaMove(Moonboard())
    app.handOperator = ["LH", "RH", "RH", "LH"]
    app.handSequence = [0, 1, 7, 9]
    assert app.get_left_hand_order() == 9


def test_get_right_hand_order() -> None:
    app = BetaMove(Moonboard())
    app.handOperator = ["LH", "RH", "RH", "LH"]
    app.handSequence = [0, 1, 7, 9]
    assert app.get_right_hand_order() == 7


def test_get_xy_from_order() -> None:
    app = setup_standard()
    assert app.get_xy_from_order(0) == (5, 4)


def tast_move_generator() -> None:
    expected = ['F5-LH', 'F5-RH', 'E8-LH', 'H10-RH', 'D12-LH',
                'E13-RH', 'B16-LH', 'D18-RH'
                ]
    assert expected == expected


gauss_data = [
    [[[5, 6], [4, 5], "LH"], .37802090861230714],
    [[[3, 6], [4, 5], "RH"], .37802090861230714],
    [[[1, 6], [4, 5], "RH"], .9285535997337063]
]


@pytest.mark.parametrize("input, expected", gauss_data)
def test_make_gaussian(input: list, expected: float) -> None:
    actual = BetaMove.make_gaussian(*input)
    assert actual == expected


success_data = [
    [[0, 5], 1.0],
    [[6, 5], 0.0],
]


@pytest.mark.parametrize("input, expected", success_data)
def test_success_rate(input: list, expected: float) -> None:
    actual = BetaMove.success_rate_by_distance(*input)
    assert actual == expected


def test_bad_climb() -> None:
    climb = Climb()
    board = Moonboard()
    app = BetaMove(board)
    with pytest.raises(Exception):
        app.match_hold_features(climb)
