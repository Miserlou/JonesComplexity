if self.max_complexity < 0:
    return
visitor = PathGraphingAstVisitor()
visitor.preorder(self.tree, visitor)
for graph in visitor.graphs.values():
    if graph.complexity() > self.max_complexity:
        text = self._error_tmpl % (graph.entity, graph.complexity())
        yield graph.lineno, 0, text, type(self)
