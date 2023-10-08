import numpy as np
from typing import Tuple, TypeVar


T = TypeVar('T', bound='Hold')


class Hold:

    # class default constructor
    def __init__(
                 self: T,
                 id: int,
                 location: Tuple[int, int],
                 orientation: int
                 ) -> None:
        # Instance Attributes
        self._id = id

        # (x, y)
        self._location = location
        # int 0-7 clockwise starting North
        self._orientation = orientation

        # (left, right)
        self._difficulties = (0, 0)
        self._features = (0, 0, 0, 0, 0, 0)

    # Setters and Getters
    def get_difficulties(self: T) -> tuple:
        return self._difficulties

    def get_right_difficulty(self: T) -> int:
        """
        return the right hand difficulty
        """
        return self._difficulties[1]

    def get_left_difficulty(self: T) -> int:
        """
        return the left hand difficulty
        """
        return self._difficulties[0]

    def get_features(self: T) -> tuple:
        """
        return the features
        """
        return self._features

    def get_location(self: T) -> Tuple[int, int]:
        return self._location

    def get_position(self: T) -> str:
        x, y = self._location
        return chr(x + ord('A')) + str(y + 1)

    def get_x(self: T) -> int:
        return self._location[0]

    def get_y(self: T) -> int:
        return self._location[1]

    def distance_to(self: T, hold: T) -> float:
        """
        Calculate the distance between this hold and another hold
        """
        diff = np.array(self._location) - np.array(hold._location)
        return np.linalg.norm(diff).item()
