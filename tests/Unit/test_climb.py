import pytest
from climb import Climb


# Construction
def test_constructor() -> None:
    climb = Climb()
    assert isinstance(climb, Climb)


def test_factory() -> None:
  
# Setters and Getters

def test_bad_column() -> None:
    climb = Climb()
    with pytest.raises(Exception):
        climb.add_hold(["Z1", False, False])
