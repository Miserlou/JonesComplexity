# -*- coding: utf-8 -*-

"""
Per-Line Complexity Metrics.

Based on https://github.com/PyCQA
MIT License.

"""

import ast
import json
import optparse
from collections import OrderedDict
from operator import itemgetter

__version__ = '0.1.2'


class LineComplexityVisitor(ast.NodeVisitor):
    """
    Calculates the number of AST nodes per line of code.

    Also calculates the median nodes/line score.

    """

    def __init__(self, *args, **kwargs):
        """Creates instance of LineComplexityVisitor."""
        super(LineComplexityVisitor, self).__init__(*args, **kwargs)
        self.count = {}

    def _median(self, items):
        sorted_list = sorted(items)
        length = len(items)
        index = (length - 1) // 2

        if length % 2 == 1:
            return sorted_list[index]
        return (sorted_list[index] + sorted_list[index + 1]) / 2.0

    def visit(self, node):
        """Recursively visit all the nodes and add up the instructions."""
        if hasattr(node, 'lineno'):
            lineno = str(node.lineno)
            self.count[lineno] = self.count.get(lineno, 0) + 1
        self.generic_visit(node)

    def sort(self):
        """Return a sorted list of line:nodes."""
        return OrderedDict(
            sorted(self.count.items(), key=itemgetter(1), reverse=True),
        )

    def score(self):
        """Calculate and return the median."""
        total = 0
        for line in self.count:
            total = total + self.count[line]

        return self._median(self.count.values())


class JonesComplexityChecker(object):
    """Jones complexity checker."""

    name = 'jones'
    version = __version__

    _line_code = 'J901'
    _line_error_tmpl = 'J901 Line {} is too complex ({})'

    _score_code = 'J902'
    _score_error_tmpl = 'J902 Overall Jones score is too complex ({})'

    max_line_complexity = 0
    max_jones_score = 0

    def __init__(self, tree, filename='(none)'):
        """Creates instance of JonesComplexityChecker."""
        self.tree = tree
        self.filename = filename  # flake8==2.0 support
        self._score = 0

    @property
    def score(self):
        """Returns the final score to user."""
        return self._score

    @staticmethod
    def _register_opt(parser, *args, **kwargs):
        """Handler to register an option for both Flake8 3.x and 2.x."""
        try:
            # Flake8 3.x registration
            parser.add_option(*args, **kwargs)
        except (optparse.OptionError, TypeError):
            # Flake8 2.x registration
            parse_from_config = kwargs.pop('parse_from_config', False)
            option = parser.add_option(*args, **kwargs)
            if parse_from_config:
                parser.config_options.append(
                    option.get_opt_string().lstrip('-'),
                )

    @classmethod
    def add_options(cls, parser):
        """Used by flake8 to add options."""
        cls._register_opt(
            parser,
            '--max-line-complexity',
            default=-1,
            action='store',
            type='int',
            help='Per line complexity threshold',
        )
        cls._register_opt(
            parser,
            '--max-jones-score',
            default=-1,
            action='store',
            type='int',
            help='Total score threshold',
        )

    @classmethod
    def parse_options(cls, options):
        """Used by flake8 to parse options."""
        cls.max_line_complexity = int(options.max_line_complexity)
        cls.max_jones_score = int(options.max_jones_score)

    def run(self):
        """Runs the complexity check."""
        if self.max_line_complexity < 0 or self.max_jones_score < 0:
            return

        visitor = LineComplexityVisitor()
        visitor.visit(self.tree)

        sorted_items = visitor.sort()
        self._score = visitor.score()

        for line, score in sorted_items.items():
            if score > self.max_line_complexity:
                text = self._line_error_tmpl.format(int(line), int(score))
                yield int(line), 0, text, type(self)

        if self._score > self.max_jones_score:
            text = self._score_error_tmpl.format(self._score)
            yield 0, 0, text, type(self)


def _parse_input():
    parser = optparse.OptionParser()
    JonesComplexityChecker.add_options(parser)
    options, args = parser.parse_args()

    return options, args


def calculate_complexity(filename, options):
    """
    Contains all complexity calculation logic.

    Receives filename and options to count complexity.
    Compiles given filename to ast, then parses passed options
    and runs the check.
    """
    with open(filename, 'rU') as module:
        code = module.read()

    tree = compile(code, filename, 'exec', ast.PyCF_ONLY_AST)
    checker = JonesComplexityChecker(tree)
    checker.parse_options(options)

    complexity = []
    for lineno, _, text, _ in checker.run():
        complexity.append('{}:{}:1: {}'.format(filename, int(lineno), text))

    return checker.score, complexity


def main():
    """Runs this module as CLI app."""
    options, args = _parse_input()
    score, sorted_items = calculate_complexity(args[0], options)

    print('Line counts:')
    print(json.dumps(sorted_items, indent=4))

    print('Jones Score: {}'.format(score))


if __name__ == '__main__':
    main()
