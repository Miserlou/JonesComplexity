import sys

import pytest

from jones_complexity import calculate_complexity


@pytest.mark.skipif(sys.version_info < (3,6),
                    reason='Requires python3.6')
@pytest.mark.parametrize('option_values,results', [
    ((1, 1), (7, 5)),
    ((5, 5), (3, 5)),
    ((15, 5), (0, 5)),
])
def test_async_await(fixture_filename, options, option_values, results):
    """Testing async python functions."""
    full_path = fixture_filename('async_await.py')

    score, lines = calculate_complexity(full_path, options(*option_values))
    expected_lines, expected_score = results

    assert score == expected_score
    assert len(lines) == expected_lines
