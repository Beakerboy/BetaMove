import argparse
import json
import numpy as np
import pandas as pd
from beta_move.beta_generator import BetaGenerator
from beta_move.climb import Climb
from beta_move.moonboard import Moonboard


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
        problem = {}
        for index in features.index:
            item = features.loc[index]
            problem[
                (
                    int(item['X_coord']),
                    int(item['Y_coord'])
                )
            ] = np.array(
                list(item['Difficulties'])
            ).astype(int)
        return problem
    
    # Load the json file
    f = open(args.filename)
    data = json.load(f)
    for id in data:
        climb = Climb.from_json(id, data[id])
        # validate climb against moonboard.
        movement = BetaGenerator.create_movement(climb)
        with open(args.output, 'a') as convert_file:
            convert_file.write(json.dumps(movement))
