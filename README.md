[![Coverage Status](https://coveralls.io/repos/github/Beakerboy/BetaMove/badge.svg?branch=dev)](https://coveralls.io/github/Beakerboy/BetaMove?branch=dev)
[![Python package](https://github.com/Beakerboy/BetaMove/actions/workflows/python-package.yml/badge.svg?branch=dev)](https://github.com/Beakerboy/BetaMove/actions/workflows/python-package.yml)

## About
BetaMove converts a MoonBoard problem into a move sequence that is similar to the predicted move sequence of climbing experts.

## Requirements

## Installation
BetaMove is currently under development, but can be installed from GitHub using `pip`.
```
pip install git+https://github.com/Beakerboy/BetaMove@dev
```

## Getting Started
A list of moonboard problems must be supplied. These can either be downloaded using the Moonboard API, or the archived data dump that is supplied with the source code can be used.

To run the program
```
python beta_move.py filename -l LEFT_HAND_DIFFICULTY -r RIGHT_HAND_DIFFICULTY -o OUTPUT
positional arguments:
  filename              A json file of climbing problems to analyze.
  -l                    A csv file that lists the difficulty score (1-9?) of each hold using the left hand.
  -r                    A csv file that lists the difficulty score (1-9?) of each hold using the right hand.
  -o OUTPUT, --output OUTPUT
                        The output file name.
```

## Objects
# Moonboard
The moonboard object manages all the holds.
# Hold
A hold is a specific hold with a location and orientation.
# Climb
A climb is a list of golds that make up a specific moonboard problem.
# BetaGenerator
The BetaGenerator creates the optimal Beta for a specific Climb.
# BetaMove
A series of hand movements between holds.

## Tests
The tests directory contains examples of how the classes can be used within other projects. There are also complete functional tests that include full working examples of creating the output file from CLI or using the module's objects.

## Contributing
Contributions are welcome. Please ensure new features include unit tests to maintain 100% coverage. All code must adhere to the [PEP8 Standards](https://peps.python.org/pep-0008/) for both formatting and naming. Method signatures must be fully annotated.
