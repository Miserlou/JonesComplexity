# -*- coding: utf-8 -*-

import subprocess

EMPTY_FILE_CONTENTS = """
# -*- coding: utf-8 -*-

\"\"\"Fake module docstring.\"\"\"
"""

BASIC_FILE_CONTENTS = """
# -*- coding: utf-8 -*-

\"\"\"Fake module docstring.\"\"\"

value = 1 + 2 / 3
"""


def test_call_main(tmpdir):
    """Covers a situation when main is called without any arguments."""
    tmp = tmpdir.join('tmp.py')
    tmp.write(EMPTY_FILE_CONTENTS)

    p = subprocess.Popen(
        [
            'python', '-m', 'jones_complexity',
            str(tmp),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, _ = p.communicate()

    assert b'J901' in stdout
    assert b'J902' not in stdout


def test_call_main_with_params(tmpdir):
    """Runs main checks with lowes thresholds possible."""
    tmp = tmpdir.join('tmp.py')
    tmp.write(BASIC_FILE_CONTENTS)

    p = subprocess.Popen(
        [
            'python', '-m', 'jones_complexity',
            '--max-line-complexity=1',
            '--max-jones-score=1',
            str(tmp),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, _ = p.communicate()

    assert b'J901' in stdout
    assert b'J902' in stdout
