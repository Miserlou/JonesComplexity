# JonesComplexity

Flake8 extension to calculate per-line complexity.

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

Shamelessly named after myself.