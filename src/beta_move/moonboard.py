import numpy as np
import pandas as pd
from pathlib import Path
from typing import Any, Dict, Tuple, Type, TypeVar


T = TypeVar('T', bound='Moonboard')


class Moonboard:

    # class default constructor
    def __init__(self: T, year: int = 2016, angle: int = 40) -> None:

        # Instance Attributes
        # hold specific atributes
        self._db: Dict[Tuple[int, int], Tuple[np.ndarray, int, int]] = {}

        # which hold is in which location
        self._location: Dict[Tuple[int, int], int] = {}

        self._angle: int = angle
        self._height: int = 18
        if year == 2016:
            base_path = Path(__file__).parent
            path = (base_path / "data/Hold_Positions_2016.csv").resolve()
            self._locations = self._transform3(path.absolute())
            path = (base_path / "data/Hold_Database.csv").resolve()
            self._db = self._transform4(path.absolute())

    def get_features(self: T, position: Tuple[int, int]) -> np.ndarray:
        """
        Return the features for the hold at a particular location
        """
        hold_id = self._locations[location]
        return self._db[hold_id][0]

    def get_rh_difficulty(self: T, position: Tuple[int, int]) -> int:
        """
        Return the right hand difficulty for the hold at a particular location
        """
        hold_id = self._locations[location]
        return self._db[hold_id][2]

    def get_lh_difficulty(self: T, location: Tuple[int, int]) -> int:
        """
        Return the left hand difficulty for the hold at a particular location
        """
        hold_id = self._locations[location]
        return self._db[hold_id][1]

    def hold_exists(self: T, position: Tuple[Any]) -> bool:
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

    def _transform3(self: T, file: Path) -> Dict[Tuple[int, int], int]:
        features = pd.read_csv(file, dtype=str)
        dict = {}
        for index in features.index:
            item = features.loc[index]
            position = item['Position']
            dict[
                self.position_to_location(position)
            ] = int(item['Hold'])
        return dict

    def _transform4(self: T, file: Path) -> Dict[Tuple[int, int], int]:
        features = pd.read_csv(file, dtype=str)
        dict = {}
        for index in features.index:
            item = features.loc[index]
            features = np.array(
                list(item['Features'])
            ).astype(int)
            left = int(item['Left'])
            right = int(item['Right'])
            dict[
                int(item['Hold'])
            ] = (features, left, right)
        return dict

    @classmethod
    def position_to_location(cls: Type[T], position: str) -> tuple:
        x = ord(position[0]) - ord('A')
        y = int(position[1:]) - 1
        return (x, y)

    @classmethod
    def coordinate_to_string(cls: Type[T], coordinate: tuple) -> str:
        return chr(coordinate[0] + ord('A')) + str(coordinate[1] + 1)
