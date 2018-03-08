"""
Per-Line Complexity Metrics.

Based on https://github.com/PyCQA
MIT License.

"""

import ast
import collections
import json
import optparse
import sys

from ast import iter_child_nodes
from collections import OrderedDict
from operator import itemgetter

__version__ = '0.1.2'

class LineComplexityVisitor(ast.NodeVisitor):
    """
    Calculates the number of AST nodes per line of code,
    and calculates the median nodes/line score.

    """

    def __init__(self, *args, **kwargs):
        super(LineComplexityVisitor, self).__init__(*args, **kwargs)
        self.count = {}

    def _median(self, items):
        sorted_list = sorted(items)
        length = len(items)
        index = (length - 1) // 2

        if (length % 2):
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
    _line_error_tmpl = "J901 Line %r is too complex (%d)"

    _score_code = 'J902'
    _score_error_tmpl = "J902 Overall Jones score is too complex (%s)"

    max_line_complexity = 0
    max_jones_score = 0

    def __init__(self, tree):
        self.tree = tree
        self._score = 0

    @property
    def score(self):
        return self._score

    @classmethod
    def add_options(cls, parser):
        parser.add_option('--max-line-complexity', default=-1, action='store',
                          type='int', help="Per line complexity threshold")
        parser.add_option('--max-jones-score', default=-1, action='store',
                          type='int', help="Total score threshold")
        parser.config_options.append('max-line-complexity')
        parser.config_options.append('max-jones-score')

    def parse_options(self, options):
        self.max_line_complexity = int(options.max_line_complexity)
        self.max_jones_score = int(options.max_jones_score)

    def run(self):
        if self.max_line_complexity < 0 or self.max_jones_score < 0:
            return

        visitor = LineComplexityVisitor()
        visitor.visit(self.tree)

        sorted_items = visitor.sort()
        self._score = visitor.score()

        for line, score in sorted_items.items():
            if score > self.max_line_complexity:
                text = self._line_error_tmpl % (int(line), int(score))
                yield line, 0, text, type(self)

        if self._score > self.max_jones_score:
            text = self._score_error_tmpl % (self._score)
            yield 0, 0, text, type(self)

def _parse_input():
    argv = sys.argv[1:]

    opar = optparse.OptionParser()
    opar.add_option('-m', '--min', dest='threshold',
                    help='minimum complexity for output', type='int',
                    default=1)
    return opar.parse_args(argv)

def calculate_complexity(filename, options):
    with open(filename, 'rU') as module:
        code = module.read()

    tree = compile(code, filename, 'exec', ast.PyCF_ONLY_AST)
    checker = JonesComplexityChecker(tree)
    checker.parse_options(options)

    complexity = []
    for lineno, _, text, check in checker.run():
        complexity.append('%s:%d:1: %s' % (filename, int(lineno), text))

    return checker.score, complexity

def main(argv=None):
    options, args = _parse_input()
    score, sorted_items = calculate_complexity(args[0])

    print("Line counts:")
    print(json.dumps(sorted_items, indent=4))

    print("Jones Score:")
    print(score)

if __name__ == '__main__':
    main(sys.argv[1:])

