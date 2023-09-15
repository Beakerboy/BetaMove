import numpy as np
from beta_move.climb import Climb
from beta_move.moonboard import Moonboard
from typing import TypeVar


T = TypeVar('T', bound='BetaMove')


class BetaMove:

    # class default constructor
    def __init__(self: T, board: Moonboard) -> None:

        # Instance Attributes
        self._board = board

    def create_movement(self: T, climb: Climb) -> list:
        # movement = []
        if climb.is_valid:
            i = 0
            x_vectors = np.zeros((10, climb.num_holds()))
            holds = climb.get_holds().sort(key = lambda x: x[1])
            for (x, y) in climb.get_holds():
                x_vectors[0:6, i] = self._board.get_features((x, y))
                x_vectors[6:8, i] = [x, y]
                i += 1
            x_vectors[8:, 0:climb.num_starts()] = np.array([[1], [0]])
            x_vectors[8:, climb.num_holds() - climb.num_finish():] = np.array([[0], [1]])

        return x_vectors
