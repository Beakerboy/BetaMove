from beta_move import BetaMove

def test_constructor() -> None:
    app = BetaMove()
    assert isinstance(app, BetaMove)
