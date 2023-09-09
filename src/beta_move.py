import argparse
import pandas as pd
import pandas.DataFrame as df
from typing import TypeVar


T = TypeVar('T', bound='BetaMove')


class BetaMove:

    #class default constructor
    def __init__(self: T) -> None:

        # Instance Attributes
        self._left = {}
        self._right = {}

    def set_left(self: T, left: df) -> None:
        self._left = left

    def set_right(self: T, right: df) -> None:
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
    LeftHandfeatures = pd.read_csv(args.left, dtype=str)
    RightHandfeatures = pd.read_csv(args.right, dtype=str)
    app.set_left(LeftHandfeatures)
    app.set_right(RightHandfeatures)
