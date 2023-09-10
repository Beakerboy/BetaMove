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
    left_hand_features = pd.read_csv(args.left, dtype=str)
    right_hand_features = pd.read_csv(args.right, dtype=str)
    rh_feature_dict = {}
    lh_feature_dict = {}
    
    for index in right_hand_features.index:
        lh_feature_item = left_hand_features.loc[index]
        lh_feature_dict[(int(lh_feature_item['X_coord']), int(lh_feature_item['Y_coord']))] = np.array(
            list(lh_feature_item['Difficulties'])).astype(int)
        rh_feature_item = right_hand_features.loc[index]
        rh_feature_dict[(int(rh_feature_item['X_coord']), int(rh_feature_item['Y_coord']))] = np.array(
            list(rh_feature_item['Difficulties'])).astype(int)

    app.set_left(lh_feature_dict)
    app.set_right(rh_feature_dict)
