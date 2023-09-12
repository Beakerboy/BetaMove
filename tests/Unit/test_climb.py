import pytest
from climb import Climb


# Construction
def test_constructor() -> None:
    climb = Climb()
    assert isinstance(climb, Climb)


def test_factory() -> None:
    data = json.load('''{
        "1": {
            "grade": "5+",
            "problem_name": "Foo",
            "moves": [
                {"Description": "A1", "IsStart": true, "IsEnd": false},
                {"Description": "A18", "IsStart": false, "IsEnd": true},
                {"Description": "A8", "IsStart": false, "IsEnd": false}
            ]
        }
    }''')
    climb = Climb.from_json(data)
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
