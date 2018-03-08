import os

import pytest


class _CheckerOptions(object):
    def __init__(self, line, total):
        self.max_line_complexity = line
        self.max_jones_score = total


@pytest.fixture(scope='session')
def fixture_filename():
    """Returns path to the fixture file."""
    def _inner_fabric(filename):
        base = os.path.dirname(__file__)
        return os.path.join(base, 'fixtures', filename)

    return _inner_fabric


@pytest.fixture(scope='session')
def options():
    def _inner_fabric(line, total):
        return _CheckerOptions(line, total)

    return _inner_fabric
