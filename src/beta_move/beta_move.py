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
            for i, (x, y) in enumerate(climb.get_holds()):
                x_vectors = np.zeros((10, n_hold))
                x_vectors[0:6, i] = self._board.get_features((x, y)) # 6 hand features
                x_vectors[6:8, i] = [x, y] #(x, y)
                # for each hold set whether it is start/end based on index (as combined_list is start:mid:end)
                x_vectors[8:, 0:climb.num_starts()] = np.array([[1], [0]])
                x_vectors[8:, climb.num_holds() - climb.num_finish():] = np.array([[0], [1]])

        return x_vectors
