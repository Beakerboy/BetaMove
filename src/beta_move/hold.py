from typing import TypeVar, Type


T = TypeVar('T', bound='Hold')


class Hold:

    # class default constructor
    def __init__(self: T, id: int) -> None:
        # Instance Attributes
        self._id = id

    def get_difficulties(self: T) -> tuple:
        pass

    def get_right_difficulty(self: T) -> int:
        pass

    def get_left_difficulty(self: T) -> int:
        pass

    def get_features(self: T) -> tuple:
        pass
    
