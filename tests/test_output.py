from jones_complexity import get_code_complexity


def test_output_count_high(capsys, fixture_contents):
    """Testing high threshold output."""
    get_code_complexity(
        fixture_contents('basic.py'),
        max_line_complexity=99,
        max_jones_score=99,
    )

    output, _ = capsys.readouterr()
    assert output == '\n'


def test_output_count_low(capsys, fixture_contents):
    """Testing low threshold output."""
    get_code_complexity(
        fixture_contents('basic.py'),
        max_line_complexity=1,
        max_jones_score=1,
    )

    output, _ = capsys.readouterr()
    assert len(output.split('\n')) == 10  # 9 errors + 1 empty line
