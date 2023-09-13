from beta_move.climb import Climb
from typing import TypeVar


T = TypeVar('T', bound='BetaMove')


class BetaMove:

    # class default constructor
    def __init__(self: T, lh: dict, rh: dict) -> None:

        # Instance Attributes

        # Difficulty assesments for each hold if using left or right hand
        self._left_features = lh
        self._right_features = rh

    def get_left(self: T) -> dict:
        return self._left_features

    def create_movement(self: T, problem: Climb) -> list:
        movement = []
        return movement
