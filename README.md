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
python beta_move.py -l LEFT_HAND_DIFFICULTY -r ] [-o OUTPUT] [-x EXTRA] directory
positional arguments:
  directory             The directory that contains your files.

optional arguments:
  -h, --help            show this help message and exit
  -v {3,4}, --version {3,4}
                        The OLE version to use.
  -o OUTPUT, --output OUTPUT
                        The output file name.
  -x EXTRA, --extra EXTRA
                        Path to exta directory settings yml file.
```

Some directory settings can be specified from a YAML file. Directory paths are relative to the project root. Users can specify creation and modification date in ISO format, class id as a UUID string, and user flags as a four byte integer.
```yaml
directories:
  .:
    clsid: 56616700-C154-11CE-8553-00AA00A1F95B
  Storage 1:
    created: "1995-11-16 17:43:44"
    clsid: 56616100-C154-11CE-8553-00AA00A1F95B
```

## Tests
The tests directory contains examples of how the classes can be used within other projects. There are also complete functional tests that include full working examples of creating the OLE file from CLI or using the module's objects.

## Contributing
Contributions are welcome. Please ensure new features include unit tests to maintain 100% coverage. All code must adhere to the [PEP8 Standards](https://peps.python.org/pep-0008/) for both formatting and naming. Method signatures must be fully annotated.


