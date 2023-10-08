import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, Tuple, TypeVar


T = TypeVar('T', bound='Hold')


class Hold:

    # class default constructor
    def __init__(
                 self: T,
                 id: str,
                 location: Tuple[int, int],
                 orientation: int
                 ) -> None:
        # Instance Attributes
        self._id = id

        # (x, y)
        self._location = location
        # int 0-7 clockwise starting North
        self._orientation = orientation

        base_path = Path(__file__).parent
        path = (base_path / "data/Hold_Database.csv").resolve()
        db = self._transform(path.absolute())
        # (left, right)
        self._difficulties = (db[id][1], db[id][2])
        self._features = db[id][0]

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

    def _transform(
                    self: T,
                    file: Path
                    ) -> Dict[
                              str,
                              Tuple[np.ndarray, int, int]
                              ]:
        data = pd.read_csv(file, dtype=str)
        dict = {}
        for index in data.index:
            item = data.loc[index]
            features = np.array(
                list(item['Features'])
            ).astype(int)
            left = int(item['Left'])
            right = int(item['Right'])
            dict[
                item['Hold']
            ] = (features, left, right)
        return dict
