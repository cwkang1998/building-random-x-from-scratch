from __future__ import annotations
from typing import List
from .node import BodyNode, Node, ParagraphNode
from tokenizer.token import Token


def match_first(tokens: List[Token], *parser_classes):
    for parser_class in parser_classes:
        parser = parser_class()
        node: Node = parser.match(tokens)
        if node:
            return node


def match_star(tokens: List[Token], parser_class):
    matched_nodes: List[Node] = []
    consumed = 0
    parser = parser_class()

    while True:
        node: Node = parser.match(tokens[consumed:])
        if node is None:
            break
        matched_nodes.append(node)
        consumed += node.consumed
    return [matched_nodes, consumed]


class ArgumentsError(SyntaxError):
    pass


class BaseParser:
    def match(self, tokens: List[Token]):
        raise NotImplementedError()


class TextParser(BaseParser):
    def match(self, tokens: List[Token]):
        if(len(tokens) > 0 and tokens[0].type == 'TEXT'):
            return Node('TEXT', tokens[0].value, consumed=1)


class EmphasisParser(BaseParser):
    def match(self, tokens: List[Token]):
        if len(tokens) >= 3:
            if(tokens[0].type == 'UNDERSCORE' and
                tokens[1].type == 'TEXT' and
               tokens[2].type == 'UNDERSCORE') or \
                (tokens[0].type == 'STAR' and
                 tokens[1].type == 'TEXT' and
                 tokens[2].type == 'STAR'):
                return Node(type='EMPHASIS', value=tokens[1].value, consumed=3)


class BoldParser(BaseParser):
    def match(self, tokens: List[Token]):
        if len(tokens) >= 5:
            if(tokens[0].type == 'UNDERSCORE' and
                tokens[1].type == 'UNDERSCORE' and
                tokens[2].type == 'TEXT' and
                tokens[3].type == 'UNDERSCORE' and
               tokens[4].type == 'UNDERSCORE') or \
                (tokens[0].type == 'STAR' and
                 tokens[1].type == 'STAR' and
                 tokens[2].type == 'TEXT' and
                 tokens[3].type == 'STAR' and
                 tokens[4].type == 'STAR'):
                return Node(type='BOLD', value=tokens[2].value, consumed=5)


class SentenceParser(BaseParser):
    def match(self, tokens: List[Token]):
        return match_first(tokens, BoldParser, EmphasisParser, TextParser)


class SentencesNewlineParser(BaseParser):
    def match(self, tokens: List[Token]):
        nodes, consumed = match_star(tokens, SentenceParser)
        # print('newline', nodes, consumed, tokens[:consumed])
        if(len(tokens) == 0):
            return
        if(consumed + 2 <= len(tokens) and
            tokens[consumed].type == 'NEWLINE' and
                tokens[consumed + 1].type == 'NEWLINE'):
            consumed += 2
            return ParagraphNode(nodes, consumed)


class SentencesEOFParser(BaseParser):
    def match(self, tokens: List[Token]):
        nodes, consumed = match_star(tokens, SentenceParser)
        # print('eof', nodes, consumed, tokens[:consumed])
        if(len(tokens) == 0):
            return
        if(consumed + 1 <= len(tokens) and
                tokens[consumed].type == 'EOF'):
            consumed += 1
            return ParagraphNode(nodes, consumed)
        elif(consumed + 2 <= len(tokens) and
             tokens[consumed].type == 'NEWLINE' and
                tokens[consumed + 1].type == 'EOF'):
            consumed += 2
            return ParagraphNode(nodes, consumed)


class ParagraphParser(BaseParser):
    def match(self, tokens):
        return match_first(tokens, SentencesNewlineParser, SentencesEOFParser)


class BodyParser(BaseParser):
    def match(self, tokens: List[Token]):
        nodes, consumed = match_star(tokens, ParagraphParser)
        if len(nodes) != 0:
            return BodyNode(paragraphs=nodes, consumed=consumed)


class Parser:
    def parse(self, tokens: List[Token]):
        body = BodyParser().match(tokens)
        if(len(tokens) == body.consumed):
            return body
        raise SyntaxError(f'{tokens[body.consumed]}')
