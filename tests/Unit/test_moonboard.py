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


def test_get_features() -> None:
    board = Moonboard()
    assert all(board.get_features((5, 4)) == [5, 4, 9, 4, 1, 1])


def test_lh_difficulty() -> None
    board = Moonboard()
    assert board.get_lh_difficulty((0, 17)) == 5
