import argparse
from beta_move.beta_move import BetaMove
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

    # Create moonboard with he specified layout
    # Create movement generator.
    app = BetaMove(transform(args.left), transform(args.right))
    # Load the json file
    f = open(args.filename)
    f_out = open(args.output, "a")
    data = json.load(f)
    for id in data:
        climb = Climb.from_json(id, data[id])
        # validate climb against moonboard.
        movement = app.create_movement(climb)
        f_out.write(movement)
