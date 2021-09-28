# `rohdeschwarz` S21 Example

This is an example of how to use the VNA instrument driver from the  [rohdeschwarz](https://github.com/Terrabits/rohdeschwarz) Python package to measure S21 and capture all data.

## Requirements

The general requirements for this project are:

- Python `2.7+` or `3.4+`
- `rohdeschwarz>=1.9.1.dev1`

This example was tested with Python `3.9.5 x64` on macOS `11.5.2` Big Sur with the exact python packages and versions listed in [requirements.txt.lock](./requirements.txt.lock).

## Install

Run the `scripts/install` bash script on Linux and macOS, or `scripts/install.bat` on Windows to install the required python packages.

## Run

### Configure Instrument Address

Before the script can be run, you must first edit `VNA_IP_ADDRESS` and/or `VNA_GPIB_ADDRESS` in `__main__.py` to match the vna address:

```python
VNA_IP_ADDRESS   = 'localhost'
VNA_GPIB_ADDRESS = 19  # requires PyVISA, NI VISA
```

As noted in the comment, GPIB control uses `PyVISA`, which requires installation and use of `NI VISA`.
`PyVISA` is already installed as a dependency of `rohdeschwarz`. Unfortunately, NI VISA will have to be installed separately.

See the [PyVISA Backend Installation](https://pyvisa.readthedocs.io/en/latest/introduction/getting.html#backend) instructions.

### Execute

To run the script from the command line:

```shell
cd path/to/rohdeschwarz_s21_example
python .  # implies __main__.py
```

### Output

You should see the following files in the `data` folder:

- 
