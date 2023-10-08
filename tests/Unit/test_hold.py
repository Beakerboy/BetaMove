from beta_move.hold import Hold


# Construction
def test_constructor() -> None:
    hold = Hold("1", (0, 0), 0)
    assert isinstance(hold, Hold)


def test_get_location() -> None:
    hold = Hold("1", (0, 0), 0)
    assert hold.get_location() == (0, 0)


def test_get_position() -> None:
    hold = Hold("1", (0, 0), 0)
    assert hold.get_position() == "A1"


def test_get_x() -> None:
    hold = Hold("1", (0, 0), 0)
    assert hold.get_x() == 0


def test_get_y() -> None:
    hold = Hold("1", (0, 2), 0)
    assert hold.get_y() == 2


def test_distance_to() -> None:
    hold1 = Hold("1", (0, 0), 0)
    hold2 = Hold("2", (3, 4), 0)
    assert hold1.distance_to(hold2) == 5.0


def test_lh_difficulty() -> None:
    hold = Hold("89", (5, 4), 0)
    assert hold.get_left_difficulty() == 8


def test_rh_difficulty() -> None:
    hold = Hold("89", (5, 4), 0)
    assert hold.get_right_difficulty() == 7


def test_difficulties() -> None:
    hold = Hold("89", (5, 4), 0)
    assert hold.get_difficulties() == (8, 7)
