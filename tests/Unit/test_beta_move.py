import pytest
from beta_move.beta_move import BetaMove

def test_constructor() -> None:
    path = "./foo.txt"
    app = BetaMove()
    assert isinstance(app, BetaMove)
