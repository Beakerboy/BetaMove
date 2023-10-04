from typing import TypeVar, Type


T = TypeVar('T', bound='Hold')


class Hold:

    # class default constructor
    def __init__(self: T, id: int) -> None:
        # Instance Attributes
        self._id = id
        self._location = (0, 0)

        # (left, right)
        self._difficulties = (0, 0)
        self._features = (0, 0, 0, 0, 0, 0)

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
    
    def distance_to(self: T, hold: T) -> float:
        """
        Calculate the distance between this hold and another hold
        """
        pass
