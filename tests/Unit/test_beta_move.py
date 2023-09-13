
import json
import numpy as np
import pandas as pd
from beta_move import BetaMove
from climb import Climb


def test_constructor() -> None:
    app = BetaMove({}, {})
    assert isinstance(app, BetaMove)


def test_lh_set() -> None:
    file = "data/hold_features_2016_LH.csv"
    features = pd.read_csv(file, dtype=str)
    dict = {}
    for index in features.index:
        item = features.loc[index]
        dict[
            (int(item['X_coord']), int(item['Y_coord']))
        ] = np.array(list(item['Difficulties'])).astype(int)
    app = BetaMove(dict, dict)
    left = app.get_left()
    assert len(left) == 140
    assert left[(0, 4)] == [4]
    assert left[(0, 10)] == [1]


def test_status() -> None:
    file = "data/hold_features_2016_LH.csv"
    features = pd.read_csv(file, dtype=str)
    lh = {}
    for index in features.index:
        item = features.loc[index]
        lh[
            (int(item['X_coord']), int(item['Y_coord']))
        ] = np.array(list(item['Difficulties'])).astype(int)
    file = "data/hold_features_2016_RH.csv"
    features = pd.read_csv(file, dtype=str)
    rh = {}
    for index in features.index:
        item = features.loc[index]
        rh[
            (int(item['X_coord']), int(item['Y_coord']))
        ] = np.array(list(item['Difficulties'])).astype(int)

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
    app = BetaMove(lh, rh)
    assert app == app
    f = open('tests/Unit/342797.json')
    data = json.load(f)
    climb = Climb.from_json("342797", data["342797"])
    assert expected == expected
    assert climb == climb
