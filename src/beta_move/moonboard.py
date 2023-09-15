import numpy as np
import pandas as pd
from typing import TypeVar


T = TypeVar('T', bound='Moonboard')


class Moonboard:

    # class default constructor
    def __init__(self: T, year: int = 2016, angle: int = 40) -> None:

        # Instance Attributes
        # Left Hand Difficulties
        self._lh: dict = {}

        # Right Hand Difficulties
        self._rh: dict = {}

        # Hold Features
        self._features = {}

        self._angle: int = angle
        self._height: int = 18
        if year == 2016:
            self._lh = self._transform("data/hold_features_2016_LH.csv")
            self._lh = self._transform("data/hold_features_2016_RH.csv")
            self._features = self._transform("data/hold_features_2016_LH.csv")

    def get_features(self: T, position: list) -> list:
        """
        Return the features for the hold at a particular location
        """
        return self._features[position]

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

    def _transform(self: T, file: str) -> dict:
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
