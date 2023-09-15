from beta_move.climb import Climb
from typing import TypeVar


T = TypeVar('T', bound='BetaMove')


class BetaMove:

    # class default constructor
    def __init__(self: T, lh: dict, rh: dict) -> None:

        # Instance Attributes

    def create_movement(self: T, problem: Climb) -> list:
        movement = []
        return movement
