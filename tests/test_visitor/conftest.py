# -*- coding: utf-8 -*-

import ast
from textwrap import dedent

import pytest


@pytest.fixture(scope='session')
def parse_ast_tree():
    """Helper function to convert code to ast."""
    def factory(code):
        tree = ast.parse(dedent(code))

        for statement in ast.walk(tree):
            for child in ast.iter_child_nodes(statement):
                child.parent = statement

        return tree

    return factory
