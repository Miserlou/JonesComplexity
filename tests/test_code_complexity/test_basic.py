# -*- coding: utf-8 -*-

import pytest

from jones_complexity import calculate_complexity


@pytest.mark.parametrize('option_values,results', [
    ((1, 1), (8, 6.5)),
    ((11, 7), (0, 6.5)),
])
def test_basic(fixture_filename, options, option_values, results):
    """Testing basic python functions."""
    full_path = fixture_filename('basic.py')

    score, lines = calculate_complexity(full_path, options(*option_values))
    expected_lines, expected_score = results

    assert score == expected_score
    assert len(lines) == expected_lines
