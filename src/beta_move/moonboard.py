from typing import TypeVar, Type


T = TypeVar('T', bound='Moonboard')


class Moonboard:

    # class default constructor
    def __init__(self: T) -> None:

        # Instance Attributes
        # Left Hand Difficulties
        self._lh = {}

        # Right Hand Difficulties
        self._rh = {}

        # Hold Features
        self._features = {}

        self._angle = 40

    def get_features(self: T, position: list) -> list:
        """
        Return the features for the hold at a particular location
        """

    def get_rh_difficulty(self: T, position: list) -> int:
        """
        Return the right hand difficulty for the hold at a particular location
        """

    def get_lh_difficulty(self: T, position: list) -> int:
        """
        Return the left hand difficulty for the hold at a particular location
        """

    def hold_exists(self: T, position: list) -> bool:
        """
        Check is a hold is present on the board at a given lication
        """

    def height(self: T) -> int:
        """
        How tall is the board
        """
        return 18

    def width(self: T) -> int:
        """
        How wide is the board
        """
        return 11
