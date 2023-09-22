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


def assert_hold_exists() -> None:
    board = Moonboard()
    assert board.hold_exists((5, 4))


def assert_hold_does_not_exist() -> None:
    board = Moonboard()
    assert not board.hold_exists((0, 0))


def test_get_features() -> None:
    board = Moonboard()
    assert all(board.get_features((5, 4)) == [5, 4, 9, 4, 1, 1])


def test_lh_difficulty() -> None:
    board = Moonboard()
    assert board.get_lh_difficulty((0, 17)) == 5


def test_rh_difficulty() -> None:
    board = Moonboard()
    assert board.get_rh_difficulty((0, 15)) == 2
