import argparse
import numpy as np
import pandas as pd
from typing import TypeVar


T = TypeVar('T', bound='BetaMove')


class BetaMove:

    #class default constructor
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
    LeftHandfeatures = pd.read_csv(args.left, dtype=str)
    RightHandfeatures = pd.read_csv(args.right, dtype=str)
    RightHandfeature_dict = {}
    LeftHandfeature_dict = {}
    
    for index in RightHandfeatures.index:
        LeftHandfeature_item = LeftHandfeatures.loc[index]
        LeftHandfeature_dict[(int(LeftHandfeature_item['X_coord']), int(LeftHandfeature_item['Y_coord']))] = np.array(
            list(LeftHandfeature_item['Difficulties'])).astype(int)
        RightHandfeature_item = RightHandfeatures.loc[index]
        RightHandfeature_dict[(int(RightHandfeature_item['X_coord']), int(RightHandfeature_item['Y_coord']))] = np.array(
            list(RightHandfeature_item['Difficulties'])).astype(int)

    app.set_left(LeftHandfeature_dict)
    app.set_right(RightHandfeature_dict)
