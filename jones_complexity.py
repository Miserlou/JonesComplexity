""" 
    Per-Line Complexity Metrics
    MIT License.
"""
from __future__ import with_statement

import optparse
import sys
from collections import defaultdict
try:
    import ast
    from ast import iter_child_nodes
except ImportError:   # Python 2.5
    from flake8.util import ast, iter_child_nodes

__version__ = '0.0.1'


class LineComplexityVisitor(ast.NodeVisitor):

    count = {}

    def visit(self, node):
        if hasattr(node, 'lineno'):
            self.count[str(node.lineno)] = self.count.get(str(node.lineno), 0) + 1
        self.generic_visit(node)

    def sort(self):
        od = collections.OrderedDict(sorted(self.count.items()))
        return json.dumps(od, indent=4)

class JonesComplexityChecker(object):
    """McCabe cyclomatic complexity checker."""
    name = 'mccabe'
    version = __version__
    _code = 'C901'
    _error_tmpl = "C901 %r is too complex (%d)"
    max_complexity = 0

    def __init__(self, tree, filename):
        self.tree = tree

    @classmethod
    def add_options(cls, parser):
        parser.add_option('--max-complexity', default=-1, action='store',
                          type='int', help="McCabe complexity threshold")
        parser.config_options.append('max-complexity')

    @classmethod
    def parse_options(cls, options):
        cls.max_complexity = int(options.max_complexity)

    def run(self):
        if self.max_complexity < 0:
            return
        visitor = LineComplexityVisitor()
        visitor.preorder(self.tree, visitor)

        for graph in visitor.graphs.values():

            if graph.complexity() > self.max_complexity:
                text = self._error_tmpl % (graph.entity, graph.complexity())
                yield graph.lineno, 0, text, type(self)


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    opar = optparse.OptionParser()
    opar.add_option("-d", "--dot", dest="dot",
                    help="output a graphviz dot file", action="store_true")
    opar.add_option("-m", "--min", dest="threshold",
                    help="minimum complexity for output", type="int",
                    default=1)

    options, args = opar.parse_args(argv)

    with open(args[0], "rU") as mod:
        code = mod.read()

    tree = compile(code, args[0], "exec", ast.PyCF_ONLY_AST)
    visitor = PathGraphingAstVisitor()
    visitor.visit(tree, visitor)

    # for graph in visitor.graphs.values():
    #     if graph.complexity() >= options.threshold:
    #         print(graph.name, graph.complexity())


if __name__ == '__main__':
    main(sys.argv[1:])

