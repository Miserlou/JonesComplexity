# JonesComplexity [![Build Status](https://travis-ci.org/Miserlou/JonesComplexity.svg)](https://travis-ci.org/Miserlou/JonesComplexity) [![Coverage Status](https://coveralls.io/repos/github/Miserlou/JonesComplexity/badge.svg)](https://coveralls.io/github/Miserlou/JonesComplexity)

Flake8 extension to calculate per-line complexity and total code density.

## Installation

```bash
$ pip install jones-complexity
```

## Usage (Standalone)

```bash
$ python -m jones_complexity --max-line-complexity 5 your_file.py
```

## Usage (flake8)

```bash
$ flake8 --max-line-complexity 15 --max-jones-score 8 yourproject
```

We do not make any assumptions on the required configuration,
so if no explicit configuration is provided, this plugin will be silent.
Enable it by setting `--max-jones-score` or `--max-line-complexity` options.

## What is this?

Because

```python
if user.get_full_name().toUpper().split(' ')[0] == 'ALICE':
    return True
```

is harder to read and maintain than

```python
if first_name == 'Alice':
    return True
```

Shamelessly named after myself, in the tradition of McCabe and Halstead.

## Options

We support two options:

- `--max-line-complexity` which sets the maximum complexity for a single line
- `--max-jones-score` which sets maximum median complexity inside a module

You can provide options via:

- a command line, this works for both standalone and `flake8` usages
- `setup.cfg` and `.flake8` files, see [docs](http://flake8.pycqa.org/en/latest/user/configuration.html)

## Examples

Itself:

```bash
$ python -m jones_complexity jones_complexity.py
[
    "jones_complexity.py:46:1: J901 Line 46 is too complex (13)",
    "jones_complexity.py:40:1: J901 Line 40 is too complex (12)",
    ...
    "jones_complexity.py:154:1: J901 Line 154 is too complex (2)",
    "jones_complexity.py:170:1: J901 Line 170 is too complex (2)"
]
Jones Score: 3
```

[PyEsprima](https://raw.githubusercontent.com/PiotrDabkowski/Js2Py/master/examples/pyesprima.py):

```bash
$ python -m jones_complexity pyesprima.py
Line counts:
[
    "pyesprima.py:4191:1: J901 Line 4191 is too complex (265)",
    "pyesprima.py:41:1: J901 Line 41 is too complex (189)",
    "pyesprima.py:4195:1: J901 Line 4195 is too complex (189)",
    "pyesprima.py:4189:1: J901 Line 4189 is too complex (164)",
    ...
    "pyesprima.py:4963:1: J901 Line 4963 is too complex (2)",
    "pyesprima.py:4978:1: J901 Line 4978 is too complex (2)",
    "pyesprima.py:4996:1: J901 Line 4996 is too complex (2)"
]
Jones Score: 9.0
```
