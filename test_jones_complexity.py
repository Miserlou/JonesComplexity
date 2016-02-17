import unittest
import sys
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from jones_complexity import get_code_complexity


_GLOBAL = """
if self.max_complexity < 0:
    return
visitor = PathGraphingAstVisitor()
visitor.preorder(self.tree, visitor)
for graph in visitor.graphs.values():
    if graph.complexity() > self.max_complexity:
        text = self._error_tmpl % (graph.entity, graph.complexity())
        yield graph.lineno, 0, text, type(self)
"""

class JonesComplexityTest(unittest.TestCase):

    def setUp(self):
        self.old = sys.stdout
        self.out = sys.stdout = StringIO()

    def tearDown(self):
        sys.sdtout = self.old

    def test_sample(self):

        # High threshold
        self.assertEqual(len(get_code_complexity(_GLOBAL, max_line_complexity=99, max_jones_score=99)), 0)

        # Low threshold
        self.assertEqual(len(get_code_complexity(_GLOBAL, max_line_complexity=1, max_jones_score=1)), 9)