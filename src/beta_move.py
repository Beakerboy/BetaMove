import argparse
import numpy as np
import pandas as pd
from typing import TypeVar


T = TypeVar('T', bound='BetaMove')


class BetaMove:

    # class default constructor
    def __init__(self: T) -> None:

        # Instance Attributes

        # Difficulty assesments for each hold if using left or right hand
        self._left_features = {}
        self._right_features = {}

    def set_left(self: T, left: dict) -> None:
        self._left_features = left

    def set_right(self: T, right: dict) -> None:
        self._right_features = right

    def get_left(self: T) -> dict:
        return self._left_features

    def create_movement(data: list) -> list:
        movement = []
        return movement

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--left",
                        help="The left hand difficulty file name.")
    parser.add_argument("-r", "--right",
                        help="The right hand difficulty file name.")
    parser.add_argument("-o", "--output",
                        help="The output file name.")
    args = parser.parse_args()
    app = BetaMove()

    def transform(file: str) -> dict:
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

    app.set_left(transform(args.left))
    app.set_right(transform(args.right))
