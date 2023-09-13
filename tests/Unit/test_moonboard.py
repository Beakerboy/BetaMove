from beta_move.moonboard import Moonboard


# Construction
def test_constructor() -> None:
    board = Moonboard()
    assert isinstance(board, Moonboard)


def test_height() -> None:
    board = Moonboard()
    assert board.height == 18


def test_width() -> None:
    board = Moonboard()
    assert board.width == 110
