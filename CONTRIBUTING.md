# How to contribute

## Dependencies

We use [`poetry`](https://github.com/sdispater/poetry) to manage the dependencies.

To install them you would need to run two commands:

```bash
poetry install
poetry develop
```

## Tests

We use `pytest` and `flake8` for quality control.
To run all tests:

```bash
poetry run pytest
```

Make sure you have followed all the steps before submitting your PR.


## Before submitting

Before submitting your code please do the following steps:

1. Run `pytest` to make sure everything was working before
2. Add any changes you want
3. Adds tests for the new changes
4. Edit documentation if you have changed something significant
5. Run `pytest` again to make sure it is still working


## Other help

You can contribute by spreading a word about this library.
It would also be a huge contribution to write
a short article on how you are using this project.
What are your best-practices?


## How to release

We use `poetry` to release this software.

That's how you can make it happen:
1. `poetry build`
2. `poetry publish`

Please, note that you must have an access
to the PyPI repository to push new versions.
