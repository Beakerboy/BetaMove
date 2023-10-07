import pytest
from beta_move.moonboard import Moonboard


# Construction
def test_constructor() -> None:
    board = Moonboard()
    assert isinstance(board, Moonboard)


def test_height() -> None:
    board = Moonboard()
    assert board.get_height() == 18


def test_width() -> None:
    board = Moonboard()
    assert board.get_width() == 11


def test_hold_exists() -> None:
    board = Moonboard()
    assert board.hold_exists((5, 4))


def test_hold_does_not_exist() -> None:
    board = Moonboard()
    assert not board.hold_exists((0, 0))


def test_get_features() -> None:
    board = Moonboard()
    assert all(board.get_features((5, 4)) == [5, 4, 9, 4, 1, 1])


difficulty_data = [
    [(5, 4), [8, 7]],
    [(4, 7), [8, 8]],
    [(0, 8), [8, 3]],
    [(7, 9), [8, 9]],
    [(3, 11), [6, 7]],
    [(4, 12), [7, 7]],
    [(2, 14), [4, 2]],
    [(1, 15), [5, 3]],
    [(3, 17), [9, 9]],
]


@pytest.mark.parametrize("input, difficulty", difficulty_data)
def test_lh_difficulty(input: tuple, difficulty: list) -> None:
    board = Moonboard()
    assert board.get_lh_difficulty(input) == difficulty[0]


@pytest.mark.parametrize("input, difficulty", difficulty_data)
def test_rh_difficulty(input: tuple, difficulty: list) -> None:
    board = Moonboard()
    assert board.get_rh_difficulty(input) == difficulty[1]


def test_position_to_location() -> None:
    assert Moonboard.position_to_location('A1') == (0, 0)
