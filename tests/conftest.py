import os

import pytest


@pytest.fixture(scope='session')
def fixture_file():
    """Returns path to the fixture file."""
    def _inner_fabric(filename):
        base = os.path.dirname(__file__)
        return os.path.join(base, 'fixtures', filename)

    return _inner_fabric


@pytest.fixture(scope='session')
def fixture_contents(fixture_file):
    """Returns fixture file contents."""
    def _inner_fabric(filename):
        full_path = fixture_file(filename)
        with open(full_path, 'r') as f:
            return f.read()

    return _inner_fabric
