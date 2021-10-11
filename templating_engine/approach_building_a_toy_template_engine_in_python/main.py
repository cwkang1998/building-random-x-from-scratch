from __future__ import annotations
from typing import Any, Dict, List, Literal, Tuple
import operator
import re
import ast

# Regex
VAR_TOKEN_START = '{{'
VAR_TOKEN_END = '}}'
BLOCK_TOKEN_START = '{%'
BLOCK_TOKEN_END = '%}'
TOK_REGEX = re.compile(
    fr"({VAR_TOKEN_START}.*?{VAR_TOKEN_END}|{BLOCK_TOKEN_START}.*?{BLOCK_TOKEN_END})"
)

# Fragments
VAR_FRAGMENT = 0
OPEN_BLOCK_FRAGMENT = 1
CLOSE_BLOCK_FRAGMENT = 2
TEXT_FRAGMENT = 3

WHITESPACE = re.compile('\\s+')


# Utils
operator_lookup = {
    '<': operator.lt,
    '<=': operator.le,
    '>': operator.gt,
    '>=': operator.ge,
    '==': operator.eq,
    '!=': operator.ne,
}


def eval_exp(expr: str) -> tuple[Literal['literal'], Any]:
    try:
        return 'literal', ast.literal_eval(expr)
    except (ValueError, SyntaxError):
        return 'name', expr


def resolve(name: str, context: Dict[str, Any]):
    if(name.startswith('..')):
        context = context.get('..', {})
        name = name[2:]

    try:
        for tok in name.split('.'):
            context = context[tok]
        return context
    except KeyError:
        raise TemplateContextError(name)


# Errors
class TemplateError(Exception):
    pass


class TemplateContextError(Exception):
    def __init__(self, context_var: str) -> None:
        self.context_var = context_var

    def __str__(self) -> str:
        return f"cannot resolve {self.context_var}"


class TemplateSyntaxError(Exception):
    def __init__(self, error_syntax: str) -> None:
        self.error_syntax = error_syntax

    def __str__(self) -> str:
        return f"{self.error_syntax} seems like invalid syntax"

# Nodes


class _Fragment(object):
    def __init__(self, raw_text: str) -> None:
        self.raw = raw_text.strip()
        self.clean = self.clean_fragment()

    def clean_fragment(self) -> str:
        if self.raw[:2] in [VAR_TOKEN_START, BLOCK_TOKEN_START]:
            return self.raw.strip()[2:-2].strip()
        return self.raw

    @property
    def type(self):
        raw_start = self.raw[:2]
        if raw_start == VAR_TOKEN_START:
            return VAR_FRAGMENT
        elif raw_start == BLOCK_TOKEN_START:
            return CLOSE_BLOCK_FRAGMENT if self.clean[:3] == 'end' else OPEN_BLOCK_FRAGMENT
        else:
            return TEXT_FRAGMENT


class _Node(object):
    '''
    Base class for tree nodes for the AST
    '''

    def __init__(self, fragment: str = None) -> None:
        self.children: List[_Node] = []
        self.creates_scope = False
        self.process_fragment(fragment)

    def process_fragment(self, fragment: str):
        pass

    def enter_scope(self):
        pass

    def exit_scope(self):
        pass

    def render(self, context) -> str:
        pass

    def render_children(self, context, children: _Node = None) -> str:
        if children is None:
            children = self.children

        def render_child(child: _Node) -> str:
            child_html = child.render(context)
            return '' if not child_html else str(child_html)

        return ''.join(map(render_child, children))


class _ScopableNode(_Node):
    def __init__(self, fragment: str) -> None:
        super().__init__(fragment=fragment)
        self.creates_scope = True


class _Root(_Node):
    def render(self, context) -> str:
        return super().render_children(context)


class _Variable(_Node):
    def process_fragment(self, fragment: str):
        self.name = fragment

    def render(self, context) -> str:
        return resolve(self.name, context)


class _Each(_ScopableNode):
    def process_fragment(self, fragment: str):
        try:
            _, it = WHITESPACE.split(fragment, 1)
            self.it = eval_exp(it)
        except ValueError:
            raise TemplateSyntaxError(fragment)

    def render(self, context) -> str:
        items = self.it[1] if self.it[0] == 'literal' else resolve(self.it[1], context)

        def render_item(item):
            return self.render_children({'..': context, 'it': item})
        return ''.join(map(render_item, items))


class _If(_ScopableNode):
    def process_fragment(self, fragment: str):
        bits = fragment.split()[1:]
        if len(bits) not in (1, 3):
            raise TemplateSyntaxError(fragment)
        self.lhs = eval_exp(bits[0])
        if len(bits) == 3:
            self.op = bits[1]
            self.rhs = eval_exp(bits[2])

    def render(self, context):
        lhs = self.resolve_side(self.lhs, context)
        if hasattr(self, 'op'):
            op = operator_lookup.get(self.op)
            if op is None:
                raise TemplateSyntaxError(self.op)
            rhs = self.resolve_side(self.rhs, context)
            exec_if_branch = op(lhs, rhs)
        else:
            exec_if_branch = operator.truth(self.lhs)
        if_branch, else_branch = self.split_children()
        return self.render_children(context, self.if_branch if exec_if_branch else self.else_branch)

    def resolve_side(self, side, context):
        return side[1] if side[0] == 'literal' else resolve(side[1], context)

    def exit_scope(self):
        self.if_branch, self.else_branch = self.split_children()

    def split_children(self):
        if_branch, else_branch = [], []
        curr = if_branch
        for child in self.children:
            if isinstance(child, _Else):
                curr = else_branch
                continue
            curr.append(child)
        return if_branch, else_branch


class _Else(_Node):
    def render(self, context):
        pass


class _Call(_Node):
    def process_fragment(self, fragment: str):
        try:
            bits = WHITESPACE.split(fragment)
            self.callable = bits[1]
            self.args, self.kwargs = self._parse_params(bits[:2])
        except (ValueError, IndexError):
            raise TemplateSyntaxError(fragment)

    def _parse_params(self, params: str) -> Tuple[List[Any], Dict[str, Any]]:
        args, kwargs = [], {}
        for param in params:
            if '=' in param:
                name, value = param.splt('=')
                kwargs[name] = eval_exp(value)
            else:
                args.append(eval_exp(params))
        return args, kwargs

    def render(self, context):
        resolved_args, resolved_kwargs = [], {}
        for kind, value in self.args:
            if kind == 'name':
                value = resolve(value, context)
            resolved_args.append(value)

        for key, (kind, value) in self.kwargs.items():
            if kind == 'name':
                value = resolve(value, context)
            resolved_kwargs[key] = value

        resolved_callable = resolve(self.callable, context)
        if hasattr(resolved_callable, '__call__'):
            return resolved_callable(*resolved_args, **resolved_kwargs)
        else:
            raise TemplateError(f"{self.callable} is not a callable")


class _Text(_Node):

    def process_fragment(self, fragment: str):
        self.text = fragment

    def render(self, context) -> str:
        return self.text


# Compilers

class Compiler(object):
    def __init__(self, template_string: str) -> None:
        self.template_string = template_string

    def each_fragment(self):
        clean_list = [e for e in TOK_REGEX.split(self.template_string) if e]
        for fragment in clean_list:
            if fragment:
                yield _Fragment(fragment)

    def compile(self):
        root = _Root()
        scope_stack = [root]
        for fragment in self.each_fragment():
            if not scope_stack:
                raise TemplateError('nesting issues')
            parent_scope = scope_stack[-1]
            if fragment.type == CLOSE_BLOCK_FRAGMENT:
                parent_scope.exit_scope()
                scope_stack.pop()
                continue
            new_node = self.create_node(fragment)
            if new_node:
                parent_scope.children.append(new_node)
                if new_node.creates_scope:
                    scope_stack.append(new_node)
                    new_node.enter_scope()
        return root

    def create_node(self, fragment: _Fragment) -> _Node:
        node_class = None
        if fragment.type == TEXT_FRAGMENT:
            node_class = _Text
        elif fragment.type == VAR_FRAGMENT:
            node_class = _Variable
        elif fragment.type == OPEN_BLOCK_FRAGMENT:
            cmd = fragment.clean.split()[0]
            if cmd == 'each':
                node_class = _Each
            elif cmd == 'if':
                node_class = _If
            elif cmd == 'else':
                node_class = _Else
            elif cmd == 'call':
                node_class = _Call
            if node_class is None:
                raise TemplateSyntaxError(fragment)
        return node_class(fragment.clean)


class Template(object):
    def __init__(self, contents: str) -> None:
        self.contents = contents
        self.root = Compiler(contents).compile()

    def render(self, **kwargs):
        return self.root.render(kwargs)


context = {
    'title': 'MY TODOS',
    'todos': [
        dict(title='grocery shopping', description='do all the shopping', done=True, followers=[]),
        dict(title='pay bills', description='pay all the bills', done=False, followers=['alex']),
        dict(title='go clubbing', description='get drunk',
             done=False, followers=['alex', 'mike', 'paul']),
    ]
}

result = Template('''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>microtemplates templates benchmark</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="author" content="alekos">
    <link href="/css/my.css" type="text/css" rel="stylesheet">
    <link href="/css/really.css" type="text/css" rel="stylesheet">
    <link href="/css/good.css" type="text/css" rel="stylesheet">
    <link href="/css/styles.css" type="text/css" rel="stylesheet">
  </head>
  <body>
    <div id="wrapper">
      <h1>{{title}}</h1>
      <h2>todos-orama</h2>
      <div id="content">
        {% each todos %}
          <div class="todo {% if it.done %}done{% end%}">
            <div class="title">{{it.title}}</div>
            <div class="description">{{it.description}}</div>
            {% if it.followers %}
              <div class="followers">
                {% each it.followers %}
                  <span class="follower">{{it}}</span>
                {% end %}
              </div>
            {% end %}
          </div>
        {% end %}
      </div>
    </dov>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js"></script>
    <script src="/js/scripts.js"></script>
  </body>
</html>''').render(**context)

print(result)
