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


def test_call_flake8(tmpdir):
    """Covers a situation when flake8 is called without any arguments."""
    tmp = tmpdir.join('tmp.py')
    tmp.write(EMPTY_FILE_CONTENTS)

    output = subprocess.check_output(
        ['flake8', str(tmp)],
        stderr=subprocess.STDOUT,
    )
    assert output == b''


def test_call_flake8_version():
    """Checks that module is registered and visible in the meta data."""
    output = subprocess.check_output(
        ['flake8', '--version'],
        stderr=subprocess.STDOUT,
    )
    assert b'jones-complexity: ' in output


def test_call_flake8_with_params(tmpdir):
    """Runs flake8 checks with lowes thresholds possible."""
    tmp = tmpdir.join('tmp.py')
    tmp.write(BASIC_FILE_CONTENTS)

    p = subprocess.Popen(
        [
            'flake8',
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
