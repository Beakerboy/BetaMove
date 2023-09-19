
import json
import numpy as np
from beta_move.beta_move import BetaMove
from beta_move.climb import Climb
from beta_move.moonboard import Moonboard


def test_constructor() -> None:
    board = Moonboard(2016)
    app = BetaMove(board)
    assert isinstance(app, BetaMove)


def test_make_gaussian() -> None:
    target = [5, 6]
    center = [4, 5]
    last_hand = "LH"
    expected = .029163226
    actual = BetaMove.makeGaussian(target, center, last_hand)
    assert actual == expected

def test_status() -> None:

    expected = [
        [5., 4., 9., 4., 1., 1., 5., 4., 1., 0.],
        [0., 2., 4., 2., 0., 0., 4., 7., 0., 0.],
        [1., 5., 2., 0., 0., 0., 0., 8., 0., 0.],
        [0., 0., 4., 9., 4., 0., 7., 9., 0., 0.],
        [0., 0., 6., 4., 4., 0., 3., 11., 0., 0.],
        [0., 3., 6., 3., 0., 0., 4., 12., 0., 0.],
        [1., 4., 3., 1., 0., 0., 2., 14., 0., 0.],
        [2., 5., 2., 1., 0., 0., 1., 15., 0., 0.],
        [2., 6., 8., 6., 2., 0., 3., 17., 0., 1.]
    ]
    results = {
        "hold_index": [0, 0, 1, 3, 4, 5, 7, 8],
        "hands": ['LH', 'RH', 'LH', 'RH', 'LH', 'RH', 'LH', 'RH'],
        "success": 98.50396893
    }
    board = Moonboard(2016)
    app = BetaMove(board)
    f = open('tests/Unit/342797.json')
    data = json.load(f)
    climb = Climb.from_json("342797", data["342797"])
    np.testing.assert_array_equal(app.create_movement(climb), results)
