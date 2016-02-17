# JonesComplexity [![Build Status](https://travis-ci.org/Miserlou/JonesComplexity.svg)](https://travis-ci.org/Miserlou/JonesComplexity)

Flake8 extension to calculate per-line complexity and total code density.

## Installation

    $ pip install jones-complexity

## Usage (Standalone)

    $ python -m jones_complexity --min 5 your_file.py

## Usage (flake8)

    $ flake8 --max-line-compexity 15 --max-jones-score 8 yourproject

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

### Examples

Itself:

    $ python jones_complexity.py jones_complexity.py
    Line counts:
    {
        "39": 19, 
        "46": 15, 
        "137": 12, 
        "115": 12, 
        [...]
        "18": 1, 
        "9": 1, 
        "148": 1
    }
    Jones Score:
    4.0

[PyEsprima](https://raw.githubusercontent.com/PiotrDabkowski/Js2Py/master/examples/pyesprima.py):

    $ p jones_complexity.py pyesprima.py 
    Line counts:
    {
        "4182": 265, 
        "3688": 190, 
        "4186": 189, 
        "48": 189, 
        "4181": 164, 
        [...]
        "1201": 1, 
        "3728": 1
    }
    Jones Score:
    9.0
