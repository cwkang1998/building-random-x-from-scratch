class BaseNode:
    pass


class Node(BaseNode):
    def __init__(self, type, value, consumed) -> None:
        self.type = type
        self.value = value
        self.consumed = consumed


class ParagraphNode(BaseNode):
    def __init__(self, sentences, consumed) -> None:
        self.sentences = sentences
        self.consumed = consumed


class BodyNode(BaseNode):
    def __init__(self, paragraphs, consumed) -> None:
        self.paragraphs = paragraphs
        self.consumed = consumed
