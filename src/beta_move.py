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

def main() -> None:
    parser = argparse.ArgumentParser()
