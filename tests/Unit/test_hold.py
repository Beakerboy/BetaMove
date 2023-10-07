from beta_move.hold import Hold


# Construction
def test_constructor() -> None:
    hold = Hold("0")
    assert isinstance(hold, Hold)
