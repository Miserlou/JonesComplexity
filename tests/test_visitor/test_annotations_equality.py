# -*- coding: utf-8 -*-

import sys

import pytest

from jones_complexity import LineComplexityVisitor

REGULAR_FUNCTION_PATTERN = """
def some(a, b):
    c = a + b
    return c
"""

ANNOTATED_FUNCTION_PATTERN = """
def some(a: int, b: int) -> int:
    c: int = a + b
    return c
"""


@pytest.mark.skipif(sys.version_info < (3, 6), reason='Requires python3.6')
def test_annotations_have_equal_complexity(parse_ast_tree):
    """Testing that annotated python functions have the same complexity."""
    regular_tree = parse_ast_tree(REGULAR_FUNCTION_PATTERN)
    annotated_tree = parse_ast_tree(ANNOTATED_FUNCTION_PATTERN)

    regular_visitor = LineComplexityVisitor()
    annotated_visitor = LineComplexityVisitor()

    regular_visitor.visit(regular_tree)
    print('---')
    annotated_visitor.visit(annotated_tree)

    assert regular_visitor.score() == annotated_visitor.score()
    assert regular_visitor.sort() == annotated_visitor.sort()
