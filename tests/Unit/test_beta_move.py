
import json
import numpy as np
import pytest
from beta_move.beta_move import BetaMove
from beta_move.climb import Climb
from beta_move.moonboard import Moonboard


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
    expected = np.array([
        [5., 4., 9., 4., 1., 1., 5., 4., 1., 0.],
        [0., 2., 4., 2., 0., 0., 4., 7., 0., 0.],
        [1., 5., 2., 0., 0., 0., 0., 8., 0., 0.],
        [0., 0., 4., 9., 4., 0., 7., 9., 0., 0.],
        [0., 0., 6., 4., 4., 0., 3., 11., 0., 0.],
        [0., 3., 6., 3., 0., 0., 4., 12., 0., 0.],
        [1., 4., 3., 1., 0., 0., 2., 14., 0., 0.],
        [2., 5., 2., 1., 0., 0., 1., 15., 0., 0.],
        [2., 6., 8., 6., 2., 0., 3., 17., 0., 1.]
    ]).T
    board = Moonboard(2016)
    app = BetaMove(board)
    f = open('tests/Unit/342797.json')
    data = json.load(f)
    climb = Climb.from_json("342797", data["342797"])
    np.testing.assert_array_equal(app.match_hold_features(climb), expected)


def test_get_all() -> None:
    expected = np.array([
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
