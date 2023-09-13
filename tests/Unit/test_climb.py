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
    assert climb.url() == "https://moonboard.com/Problems/View/1/foo"


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


def test_too_many_starts() -> None:
    climb = Climb()
    climb.add_hold(["A1", True, False])
    climb.add_hold(["A2", True, False])
    with pytest.raises(Exception):
        climb.add_hold(["A3", True, False])


def test_too_many_ends() -> None:
    climb = Climb()
    climb.add_hold(["A18", False, True])
    climb.add_hold(["B18", False, True])
    with pytest.raises(Exception):
        climb.add_hold(["C18", False, True])


def test_too_many_holds() -> None:
    climb = Climb()
    for i in range(13):
        climb.add_hold(["A" + str(i + 1), False, False])
    with pytest.raises(Exception):
        climb.add_hold(["A15", False, False])
        pytest.fail("Should have 14 holds. Have " + str(climb.num_holds()))
