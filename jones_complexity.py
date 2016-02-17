""" 
    Per-Line Complexity Metrics
    Based on https://github.com/PyCQA
    MIT License.
"""
from __future__ import with_statement

from operator import itemgetter
import collections
import json
import optparse
import sys

from collections import OrderedDict

try:
    import ast
    from ast import iter_child_nodes
except ImportError:   # Python 2.5
    from flake8.util import ast, iter_child_nodes

__version__ = '0.1.1'

class LineComplexityVisitor(ast.NodeVisitor):
    """
    Calculates the number of AST nodes per line of code,
    and calculates the median nodes/line score.

    """

    count = {}

    def visit(self, node):
        """
        Recursively visit all the nodes and add up the instructions.
        """

        if hasattr(node, 'lineno'):
            self.count[str(node.lineno)] = self.count.get(str(node.lineno), 0) + 1
        self.generic_visit(node)

    def sort(self):
        """
        Return a sorted list of line:nodes.
        """
        od = sorted_x = OrderedDict(sorted(self.count.items(), key=itemgetter(1), reverse=True))
        return od

    def score(self):
        """
        Calculate and return the median.

        """

        total = 0
        for line in self.count:
            total = total + self.count[line]

        def median(lst):
            sortedLst = sorted(lst)
            lstLen = len(lst)
            index = (lstLen - 1) // 2

            if (lstLen % 2):
                return sortedLst[index]
            else:
                return (sortedLst[index] + sortedLst[index + 1])/2.0

        return median(self.count.values())

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

    def __init__(self, tree, filename):
        self.tree = tree

    @classmethod
    def add_options(cls, parser):
        parser.add_option('--max-line-complexity', default=-1, action='store',
                          type='int', help="Per line complexity threshold")
        parser.add_option('--max-jones-score', default=-1, action='store',
                          type='int', help="Total score threshold")
        parser.config_options.append('max-line-complexity')
        parser.config_options.append('max-jones-score')

    @classmethod
    def parse_options(cls, options):
        cls.max_line_complexity = int(options.max_line_complexity)
        cls.max_jones_score = int(options.max_jones_score)

    def run(self):
        if self.max_line_complexity < 0 or self.max_jones_score < 0:
            return

        visitor = LineComplexityVisitor()
        visitor.visit(self.tree)

        sorted_items = visitor.sort()
        total_score = visitor.score()

        for line, score in sorted_items.items():

            if score > self.max_line_complexity:
                text = self._line_error_tmpl % (int(line), int(score))
                yield line, 0, text, type(self)     

        if total_score > self.max_jones_score:
            text = self._score_error_tmpl % (total_score)
            yield 0, 0, text, type(self)

def get_code_complexity(code, max_line_complexity=15, max_jones_score=10, filename='stdin'):
    try:
        tree = compile(code, filename, "exec", ast.PyCF_ONLY_AST)
    except SyntaxError:
        e = sys.exc_info()[1]
        sys.stderr.write("Unable to parse %s: %s\n" % (filename, e))
        return 0

    complx = []

    checker = JonesComplexityChecker(tree, filename)
    checker.max_line_complexity = max_line_complexity
    checker.max_jones_score = max_jones_score

    for lineno, offset, text, check in checker.run():
        complx.append('%s:%d:1: %s' % (filename, int(lineno), text))

    print('\n'.join(complx))
    return complx

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    opar = optparse.OptionParser()
    opar.add_option("-m", "--min", dest="threshold",
                    help="minimum complexity for output", type="int",
                    default=1)

    options, args = opar.parse_args(argv)

    with open(args[0], "rU") as mod:
        code = mod.read()

    tree = compile(code, args[0], "exec", ast.PyCF_ONLY_AST)
    visitor = LineComplexityVisitor()
    visitor.visit(tree)

    sorted_items = visitor.sort()
    score = visitor.score()

    print("Line counts:")
    print(json.dumps(sorted_items, indent=4))

    print("Jones Score:")
    print(score)

if __name__ == '__main__':
    main(sys.argv[1:])

