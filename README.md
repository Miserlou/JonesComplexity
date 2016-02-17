# JonesComplexity

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