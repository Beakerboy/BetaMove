from beta_move.moonboard import Moonboard


# Construction
def test_constructor() -> None:
    board = Moonboard()
    assert isinstance(board, Moonboard)
