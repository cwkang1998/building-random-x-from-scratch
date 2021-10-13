from parser.node import BodyNode, Node, ParagraphNode


class BaseVisitor:
    def visit(self, node):
        raise NotImplementedError()


class TextVisitor(BaseVisitor):
    def visit(self, node: Node):
        return node.value


class EmphasisVisitor(BaseVisitor):
    def visit(self, node: Node):
        return f"<em>{node.value}<em>"


class BoldVisitor(BaseVisitor):
    def visit(self, node: Node):
        return f"<strong>{node.value}<strong>"


class SentenceVisitor(BaseVisitor):
    SENTENCE_VISITOR = {
        "BOLD": BoldVisitor(),
        "EMPHASIS": EmphasisVisitor(),
        "TEXT": TextVisitor()
    }

    def visit(self, node: Node):
        visitor = self.SENTENCE_VISITOR.get(node.type, None)
        if(visitor):
            return visitor.visit(node)
        raise SyntaxError("Invalid sentence node type.")


class ParagraphVisitor(BaseVisitor):
    sentenceVisitor = SentenceVisitor()

    def visit(self, node: ParagraphNode):
        res = "".join([self.sentenceVisitor.visit(sentence) for sentence in node.sentences])
        return f"<p>{res}</p>"


class BodyVisitor(BaseVisitor):
    paragraphVisitor = ParagraphVisitor()

    def visit(self, node: BodyNode):
        return "".join([self.paragraphVisitor.visit(p) for p in node.paragraphs])
