from beta_move.climb import Climb
from beta_move.moonboard import Moonboard
from typing import TypeVar


T = TypeVar('T', bound='BetaMove')


class BetaMove:

    # class default constructor
    def __init__(self: T, board: Moonboard) -> None:

        # Instance Attributes

    def create_movement(self: T, problem: Climb) -> list:
        movement = []
        return movement
