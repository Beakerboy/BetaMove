import json
import pytest
from beta_move.climb import Climb


# Construction
def test_constructor() -> None:
    climb = Climb()
    assert isinstance(climb, Climb)


def test_factory() -> None:
    data = json.loads('''{
        "grade": "5+",
        "problem_name": "Foo",
        "moves": [
            {"Description": "A1", "IsStart": true, "IsEnd": false},
            {"Description": "A18", "IsStart": false, "IsEnd": true},
            {"Description": "A8", "IsStart": false, "IsEnd": false}
        ]
    }''')
    climb = Climb.from_json("1", data)
    assert climb.get_name() == "Foo"


# Setters and Getters

position_data = [
    "Z1", "a9", "7", "A19"
]


@pytest.mark.parametrize("data", position_data)
def test_bad_column(data: str) -> None:
    climb = Climb()
    with pytest.raises(Exception):
        climb.add_hold([data, False, False])


def test_bad_end() -> None:
    climb = Climb()
    with pytest.raises(Exception):
        climb.add_hold(["A16", False, True])


def test_bad_start() -> None:
    climb = Climb()
    with pytest.raises(Exception):
        climb.add_hold(["A16", True, False])


bad_id_data = [
    "Z1", "01", "0", "foo"
]


@pytest.mark.parametrize("data", bad_id_data)
def test_bad_id(data: str) -> None:
    climb = Climb()
    with pytest.raises(Exception):
        climb.set_id("01")
