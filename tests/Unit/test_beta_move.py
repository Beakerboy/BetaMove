from beta_move import BetaMove


def test_constructor() -> None:
    app = BetaMove()
    assert isinstance(app, BetaMove)

def test_lh_set() -> None:

def test_status() ->None:
    input = {"342797": {"problem_name": "CHATS", "info": ["Movement Crew", "16 climbers have repeated this problem", "6B+ (User grade 6B+)", "Feet follow hands", ""], "url": "https://moonboard.com/Problems/View/342797/chats", "num_empty": 1, "num_stars": 2, "moves": [{"Id": 1922790, "Description": "F5", "IsStart": true, "IsEnd": false}, {"Id": 1922791, "Description": "E8", "IsStart": false, "IsEnd": false}, {"Id": 1922792, "Description": "H10", "IsStart": false, "IsEnd": false}, {"Id": 1922793, "Description": "D12", "IsStart": false, "IsEnd": false}, {"Id": 1922794, "Description": "E13", "IsStart": false, "IsEnd": false}, {"Id": 1922795, "Description": "A9", "IsStart": false, "IsEnd": false}, {"Id": 1922796, "Description": "C15", "IsStart": false, "IsEnd": false}, {"Id": 1922797, "Description": "B16", "IsStart": false, "IsEnd": false}, {"Id": 1922798, "Description": "D18", "IsStart": false, "IsEnd": true}], "grade": "6B+", "UserGrade": "6B+", "isBenchmark": false, "repeats": 16, "ProblemType": null, "IsMaster": false, "setter": {"Id": "1B5E4B63-91A0-4792-88AC-EEFFE4C027D4", "Nickname": "Movement Crew", "Firstname": "Movement", "Lastname": "Crew", "City": "Boulder", "Country": "USA", "ProfileImageUrl": "/Content/Account/Images/default-profile.png?637231832387360726", "CanShareData": true}}}

   expected = [[ 5., 4.,  9.,  4. , 1.,  1.,  5.,  4.,  1.,  0.],
               [ 0.,  2.,  4.,  2.,  0.,  0.,  4.,  7.,  0.,  0.],
               [ 1.,  5.,  2.,  0.,  0.,  0.,  0.,  8.,  0.,  0.],
               [ 0.,  0.,  4.,  9.,  4.,  0.,  7.,  9.,  0.,  0.],
               [ 0.,  0.,  6.,  4.,  4.,  0.,  3., 11.,  0.,  0.],
               [ 0.,  3.,  6.,  3.,  0.,  0.,  4., 12.,  0.,  0.],
               [ 1.,  4.,  3.,  1.,  0.,  0.,  2., 14.,  0.,  0.],
               [ 2.,  5.,  2.,  1.,  0.,  0.,  1., 15.,  0.,  0.],
               [ 2.,  6.,  8.,  6.,  2.,  0.,  3., 17.,  0.,  1.]]

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
                    "Id": 2119229
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
