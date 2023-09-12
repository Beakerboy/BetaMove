import argparse
import json
import numpy as np
import pandas as pd
from climb import Climb
from typing import TypeVar


T = TypeVar('T', bound='BetaMove')


class BetaMove:

    # class default constructor
    def __init__(self: T, lh: dict, rh: dict) -> None:

        # Instance Attributes

        # Difficulty assesments for each hold if using left or right hand
        self._left_features = lh
        self._right_features = rh

    def get_left(self: T) -> dict:
        return self._left_features

    def create_movement(self: T, problem: Climb) -> list:
        movement = []
        return movement


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("-l", "--left",
                        help="The left hand difficulty file name.")
    parser.add_argument("-r", "--right",
                        help="The right hand difficulty file name.")
    parser.add_argument("-o", "--output",
                        help="The output file name.")
    args = parser.parse_args()

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

    app = BetaMove(transform(args.left), transform(args.right))
    # Load the json file
    f = open(args.filename)
    data = json.load(f)
    for id in data:
        climb = Climb.from_json(id, data[id])
        movement = app.create_movement(climb)
        # write movement to output
