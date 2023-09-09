import argparse
import pandas as pd
from typing import TypeVar


T = TypeVar('T', bound='BetaMove')


class BetaMove:

    #class default constructor
    def __init__(self: T) -> None:

        # Instance Attributes
        self._left = {}
        self._right = {}

    def set_left(left: df) -> None:
        self._left = left

    def set_right(left: df) -> None:
        self._right = right

def main() -> None:
    parser = argparse.ArgumentParser()
    app = new BetaMove()
    LeftHandfeatures = pd.read_csv(left_hold_feature_path, dtype=str)
    RightHandfeatures = pd.read_csv(right_hold_feature_path, dtype=str)
    app.set_left(LeftHandfeatures)
    app.set_right(RightHandfeatures)
