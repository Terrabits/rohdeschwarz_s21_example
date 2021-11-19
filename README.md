# `rohdeschwarz` S21 Example

This is an example of how to use the VNA instrument driver from the  [rohdeschwarz](https://github.com/Terrabits/rohdeschwarz) Python package to measure antenna S21 vs frequency and position.

## Requirements

The general requirements for this project are:

-   Python `2.7+` or `3.4+`
-   `rohdeschwarz>=1.9.1.dev1`

This example was tested with Python `3.9.5 x64` on macOS `11.5.2` Big Sur with the exact python packages and versions listed in [requirements.txt.lock](./requirements.txt.lock).

## Clone Repository

Assuming `git` is installed, you can clone the repository locally by executing the following:

```shell
cd path/for/clone
git clone https://github.com/Terrabits/rohdeschwarz_s21_example.git
```

## Scripts

There are developer scripts for common actions in the [scripts/](./scripts) folder.

For Windows users, run the `.bat` version of the desired script.

A bash version of each script is also provided for Bash users (e.g. macOS and Linux).

## Install

Run `scripts/install[.bat]` to install the required python packages.

## Run

The entry point for execution is [__main__.py](./__main__.py).

### Configure Instrument Address

Before `__main__.py` can be run, you must first edit `VNA_IP_ADDRESS` or `VNA_GPIB_ADDRESS` to match your current configuration:

```python
VNA_IP_ADDRESS   = 'localhost'
VNA_GPIB_ADDRESS = 20  # requires PyVISA, NI VISA
```

As noted in the comment, GPIB control uses `PyVISA`, which requires installation and use of `NI VISA`.
`PyVISA` is already installed as a dependency of `rohdeschwarz`. Unfortunately, NI VISA will have to be installed separately.

See the [PyVISA Backend Installation](https://pyvisa.readthedocs.io/en/latest/introduction/getting.html#backend) instructions.

### Execute

To execute, either run `scripts/start[.bat]` or execute the following from the command line:

```shell
cd path/to/rohdeschwarz_s21_example
python .  # implies __main__.py
```

### Output

Progress (frequency, position) is printed to `stdout` as follows:

```comment
freq: 1000000000.0
  position: 1
  position: 2
  position: 3
  position: 4
  position: 5
freq: 2000000000.0
  position: 1
  position: 2
  position: 3
  position: 4
  position: 5
freq: 3000000000.0
  position: 1
  position: 2
  position: 3
  position: 4
  position: 5
freq: 4000000000.0
  position: 1
  position: 2
  position: 3
  position: 4
  position: 5
freq: 5000000000.0
  position: 1
  position: 2
  position: 3
  position: 4
  position: 5
freq: 6000000000.0
  position: 1
  position: 2
  position: 3
  position: 4
  position: 5
freq: 7000000000.0
  position: 1
  position: 2
  position: 3
  position: 4
  position: 5
freq: 8000000000.0
  position: 1
  position: 2
  position: 3
  position: 4
  position: 5
```

A csv file is also created in `data/data.csv`. The file format is:

```comment
freq_Hz, position, mag(s21), phase_rad(s21)
```

The output can be cleaned by running `scripts/clean[.bat]`.
