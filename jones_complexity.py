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

__version__ = '0.0.1'


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
        return json.dumps(od, indent=4)

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
    _code = 'C987'
    _error_tmpl = "C987 %r is too complex (%d)"
    max_line_complexity = 0

    def __init__(self, tree, filename):
        self.tree = tree

    @classmethod
    def add_options(cls, parser):
        parser.add_option('--max-line-complexity', default=-1, action='store',
                          type='int', help="Per line complexity threshold")
        parser.config_options.append('max-line-complexity')

    @classmethod
    def parse_options(cls, options):
        cls.max_line_complexity = int(options.max_line_complexity)

    def run(self):
        if self.max_complexity < 0:
            return
        visitor = LineComplexityVisitor()
        visitor.preorder(self.tree, visitor)

        for graph in visitor.graphs.values():

            if graph.complexity() > self.max_line_complexity:
                text = self._error_tmpl % (graph.entity, graph.complexity())
                yield graph.lineno, 0, text, type(self)


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
    print(sorted_items)

    print("Jones Score:")
    print(score)

if __name__ == '__main__':
    main(sys.argv[1:])

