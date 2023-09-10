import argparse
import numpy as np
import pandas as pd
from typing import TypeVar


T = TypeVar('T', bound='BetaMove')


class BetaMove:

    # class default constructor
    def __init__(self: T) -> None:

        # Instance Attributes
        self._left = {}
        self._right = {}

    def set_left(self: T, left: dict) -> None:
        self._left = left

    def set_right(self: T, right: dict) -> None:
        self._right = right


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
    lh_features = pd.read_csv(args.left, dtype=str)
    right_hand_features = pd.read_csv(args.right, dtype=str)

    def transform(features):
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

    app.set_left(transform(lh_features))
    app.set_right(transform(rh_features))
