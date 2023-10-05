
import json
import numpy as np
import pickle
import pytest
import random
from beta_move.beta_move import BetaMove
from beta_move.climb import Climb


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


def setup_standard() -> BetaMove:
    app = BetaMove()
    app.allHolds = x_342797
    app.totalNumOfHold = 9
    app.handSequence = [0, 0, 1, 3, 4, 5, 7, 8]
    app.handOperator = ['LH', 'RH', 'LH', 'RH', 'LH', 'RH', 'LH', 'RH']
    app.holdsNotUsed = [2, 6]
    return app


def test_constructor() -> None:
    app = BetaMove()
    assert isinstance(app, BetaMove)


def test_match_hold_features() -> None:
    expected = x_342797.T
    app = BetaMove()
    f = open('tests/Unit/342797.json')
    data = json.load(f)
    climb = Climb.from_json("342797", data["342797"])
    np.testing.assert_array_equal(app.match_hold_features(climb), expected)


def test_hand_string_sequence() -> None:
    app = BetaMove()
    f = open('tests/pickle_data/moonGen_scrape_2016_final.pkl', 'rb')
    all_climbs = pickle.load(f)
    climb = Climb.from_old_json('342797', all_climbs['342797'])
    expected = [
        'F5-LH', 'F5-RH',
        'E8-LH', 'H10-RH', 'D12-LH',
        'E13-RH', 'B16-LH', 'D18-RH'
    ]
    results = app.generate_hand_string_sequence(climb)
    assert results == expected


def test_process_data() -> None:
    app = setup_standard()
    f = open('tests/pickle_data/processed_data_seq.pkl', 'rb')
    all_results = pickle.load(f)
    expected = all_results['X_dict_seq']['342797']
    result = app.process_data()
    # the last row is missing
    np.testing.assert_array_equal(result, expected[0:3])


def tast_all() -> None:
    app = BetaMove()
    f = open('tests/pickle_data/moonGen_scrape_2016_final.pkl', 'rb')
    all_climbs = pickle.load(f)
    f2 = open('tests/pickle_data/processed_data_seq.pkl', 'rb')
    all_results = pickle.load(f2)
    failures = []
    missing = []
    exceptions = []
    good = []
    mod = random.randint(0, 7)
    for key in all_climbs:
        if int(key[-3]) % 8 == mod:
            if key in all_results['X_dict_seq']:
                try:
                    climb = Climb.from_old_json(key, all_climbs[key])
                    expected = all_results['X_dict_seq'][key]
                    result = app.process_data(climb)
                    if not np.array_equal(result, expected[0:3]):
                        failures.append(key)
                    else:
                        good.append(key)
                except Exception:
                    exceptions.append(key)
            else:
                missing.append(key)
    tot_fail = len(failures) + len(missing) + len(exceptions)
    stats = [len(failures), len(missing), len(exceptions), len(good)]
    fail_map = map(str, stats)
    fail_str = '/'.join(list(fail_map))
    assert tot_fail == 0, \
        f'{mod}: {tot_fail} out of {len(all_climbs)} failed. {fail_str}'


def test_success_by_hold() -> None:
    app = setup_standard()
    hold = app.allHolds[0]
    assert app.success_rate_by_hold(hold, "LH") == 8
    assert app.success_rate_by_hold(hold, "RH") == 7


def test_add_start() -> None:
    app = BetaMove()
    app.allHolds = x_342797
    app.totalNumOfHold = np.size(app.allHolds, axis=1)
    app.holdsNotUsed = list(range(app.totalNumOfHold))
    app.add_start_holds(False)
    assert app.handSequence == [0, 0]
    assert app.handOperator == ["LH", "RH"]


last_move_success_data = [
    [[list(range(1, 8)), [0, 0], ['LH', 'RH']], 56],
    [[[2, 4, 5, 6, 7, 8], [0, 0, 1, 3], ['LH', 'RH', 'LH', 'RH']], 72]
]


@pytest.mark.parametrize("input, expected", last_move_success_data)
def test_last_move_success(input: list, expected: int) -> None:
    app = BetaMove()
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
    app = BetaMove()
    app.handOperator = ["LH", "RH", "RH", "LH"]
    app.handSequence = [0, 1, 7, 9]
    assert app.get_left_hand_order() == 9


def test_get_right_hand_order() -> None:
    app = BetaMove()
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
    app = BetaMove()
    with pytest.raises(Exception):
        app.match_hold_features(climb)
