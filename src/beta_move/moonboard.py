import numpy as np
import pandas as pd
from typing import Any, TypeVar


T = TypeVar('T', bound='Moonboard')


class Moonboard:

    # class default constructor
    def __init__(self: T, year: int = 2016, angle: int = 40) -> None:

        # Instance Attributes
        # Left Hand Difficulties
        self._lh: dict[tuple[int, int], int] = {}

        # Right Hand Difficulties
        self._rh: dict[tuple[int, int], int] = {}

        # Hold Features
        self._features: dict[tuple[int, int], np.ndarray] = {}

        self._angle: int = angle
        self._height: int = 18
        if year == 2016:
            self._lh = self._transform2("data/hold_features_2016_LH.csv")
            self._rh = self._transform2("data/hold_features_2016_RH.csv")
            self._features = self._transform("data/hold_features.csv")

    def get_features(self: T, position: tuple[int, int]) -> np.ndarray:
        """
        Return the features for the hold at a particular location
        """
        return self._features[position]

    def get_rh_difficulty(self: T, position: tuple[int, int]) -> int:
        """
        Return the right hand difficulty for the hold at a particular location
        """
        return self._rh[position]

    def get_lh_difficulty(self: T, position: tuple[int, int]) -> int:
        """
        Return the left hand difficulty for the hold at a particular location
        """
        return self._lh[position]

    def hold_exists(self: T, position: tuple[Any]) -> bool:
        """
        Check a hold is present on the board at a given location
        """
        return position in self._features

    def get_height(self: T) -> int:
        """
        How tall is the board
        """
        return self._height

    def get_width(self: T) -> int:
        """
        How wide is the board
        """
        return 11

    def _transform(self: T, file: str) -> dict[tuple[int, int], np.ndarray]:
        features = pd.read_csv(file, dtype=str)
        dict = {}
        for index in features.index:
            item = features.loc[index]
            dict[
                (
                    int(item['X_coord']),
                    int(item['Y_coord'])
                )
            ] = np.array(
                list(item['Difficulties'])
            ).astype(int)
        return dict

    def _transform2(self: T, file: str) -> dict[tuple[int, int], int]:
        features = pd.read_csv(file, dtype=str)
        dict = {}
        for index in features.index:
            item = features.loc[index]
            dict[
                (
                    int(item['X_coord']),
                    int(item['Y_coord'])
                )
            ] = int(item['Difficulties'])
        return dict
