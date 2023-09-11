import pandas as pd
from beta_move import BetaMove


def test_constructor() -> None:
    app = BetaMove()
    assert isinstance(app, BetaMove)

def test_lh_set() -> None:
    file = "../data/hold_features_2016_LH.csv"
    features = pd.read_csv(file, dtype=str)
    dict = {}
    for index in features.index:
        item = features.loc[index]
        dict[(int(item['X_coord']), int(item['Y_coord']))] = np.array(list(item['Difficulties'])).astype(int)
    app.set_left(transform(args.left))
    assert app.get_left() == 3

def test_status() ->None:
    expected = [
        [ 5., 4.,  9.,  4. , 1.,  1.,  5.,  4.,  1.,  0.],
        [ 0.,  2.,  4.,  2.,  0.,  0.,  4.,  7.,  0.,  0.],
        [ 1.,  5.,  2.,  0.,  0.,  0.,  0.,  8.,  0.,  0.],
        [ 0.,  0.,  4.,  9.,  4.,  0.,  7.,  9.,  0.,  0.],
        [ 0.,  0.,  6.,  4.,  4.,  0.,  3., 11.,  0.,  0.],
        [ 0.,  3.,  6.,  3.,  0.,  0.,  4., 12.,  0.,  0.],
        [ 1.,  4.,  3.,  1.,  0.,  0.,  2., 14.,  0.,  0.],
        [ 2.,  5.,  2.,  1.,  0.,  0.,  1., 15.,  0.,  0.],
        [ 2.,  6.,  8.,  6.,  2.,  0.,  3., 17.,  0.,  1.]
    ]
    app = BetaMove()

def test_misc() -> None:
    input = {
        "367894": {
            "problem_name": "TALL POPPY",
            "info": [
                "halladay",
                "Be the first to repeat this problem",
                "6C+",
                "Feet follow hands",
                ""
            ],
            "url": "https://moonboard.com/Problems/View/367894/tall-poppy",
            "num_empty": 3,
            "num_stars": 0,
            "moves": [
                {
                    "Id": 2119224,
                    "Description": "F5",
                    "IsStart": true,
                    "IsEnd": false
                },
                {
                    "Id": 2119225,
                    "Description": "G2",
                    "IsStart": true,
                    "IsEnd": false
                },
                {
                    "Id": 2119226,
                    "Description": "H10",
                    "IsStart": false,
                    "IsEnd": false
                },
                {
                    "Id": 2119227,
                    "Description": "B11",
                    "IsStart": false,
                    "IsEnd": false
                },
                {
                    "Id": 2119228,
                    "Description": "E15",
                    "IsStart": false,
                    "IsEnd": false
                },
                {
                    "Id": 2119229,
                    "Description": "D18",
                    "IsStart": false,
                    "IsEnd": true
                },
                {
                    "Id": 2119230,
                    "Description": "E8",
                    "IsStart": false,
                    "IsEnd": false
                }
            ],
            "grade": "6C+",
            "UserGrade": null,
            "isBenchmark": false,
            "repeats": 0,
            "ProblemType": null,
            "IsMaster": false,
            "setter": {
                "Id": "93A38FE2-1B2B-4B0F-9B70-9A77BAE976B8",
                "Nickname": "halladay",
                "Firstname": "Jason",
                "Lastname": "Halladay",
                "City": "Los Alamos",
                "Country": "United States",
                "ProfileImageUrl": "/Content/Account/Users/Profile/93A38FE2-1B2B-4B0F-9B70-9A77BAE976B8.gif?637231996892206329",
                "CanShareData": true
            }
        }
    }
