import sys
import operator
from pprint import PrettyPrinter
from typing import Any, Dict, Iterator, List


# -- Utils
def pp(obj):
    return PrettyPrinter(indent=4).pprint(obj)


def fail(s):
    print(s)
    sys.exit(-1)


class InterpreterObject(object):
    def __init__(self, value: str) -> None:
        self.value = value

    def __repr__(self) -> str:
        return self.value


class Symbol(InterpreterObject):
    pass


class Lambda(InterpreterObject):
    def __init__(self, arguments, code) -> None:
        self.arguments = arguments
        self.code = code

    def __repr__(self) -> str:
        return f"(lambda ({self.arguments}) ({self.code})"


# -- Parser
def tokenize(s: str):
    ret = []
    in_string = False
    current_word = ""

    for i, char in enumerate(s):
        # Handle string quotes
        # If its not in_string (there was no quote before),
        # Then mark it as a string (and thus a token).
        # Else it'll just be the end of a string
        if char == "'":
            if in_string is False:
                in_string = True
                current_word += char
            else:
                in_string = False
                current_word += char
                ret.append(current_word)
                current_word = ''

        elif in_string is True:
            current_word += char

        elif char in ['\t', '\n', ' ']:
            continue

        elif char in ['(', ')']:
            ret.append(char)

        else:
            current_word += char
            if i < len(s) - 1 and s[i + 1] in ['(', ')', ' ', '\n', '\t']:
                ret.append(current_word)
                current_word = ''

    return ret


def is_integer(s: str) -> bool:
    try:
        int(s)
        return True
    except ValueError:
        return False


def is_float(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False


def is_string(s: str) -> bool:
    if s[0] == "'" and s[-1] == "'":
        return True
    return False


def do_parse(tokens: Iterator[str]):
    ret = []

    for token in tokens:
        if token == '(':
            ret.append(do_parse(tokens))
        elif token == ')':
            return ret
        elif is_integer(token):
            ret.append(int(token))
        elif is_float(token):
            ret.append(float(token))
        elif is_string(token):
            # Essentially the indexing is for removing the quotes
            ret.append(token[1:][0:-1])
        else:
            ret.append(Symbol(token))


def parse(tokens: List[str]):
    if(len(tokens) == 0):
        return

    itert = iter(tokens)
    token = next(itert)

    if token != '(':
        fail(f"Unexpected token {token}")

    return do_parse(itert)


# -- Interpreter
def eval(expr: Any, environment: Dict[str, Any]) -> Any:
    if isinstance(expr, int):
        return expr
    elif isinstance(expr, float):
        return expr
    elif isinstance(expr, str):
        return expr
    elif isinstance(expr, Symbol):
        if expr.value not in environment:
            fail(f"Couldn't find symbol {expr.value}")
        return environment[expr.value]
    elif isinstance(expr, list):
        if(isinstance(expr[0], Symbol)):
            if(expr[0].value == 'lambda'):
                arg_names = expr[1]
                code = expr[2]
                return Lambda(arg_names, code)
            elif expr[0].value == 'if':
                condition = expr[1]
                then = expr[2]
                _else = None
                if len(expr) == 4:
                    _else = expr[3]
                if eval(condition, environment):
                    return eval(then, environment)
                elif _else is not None:
                    return eval(_else, environment)
            elif expr[0].value == 'let':
                name = expr[1]
                value = eval(expr[2], environment)
                environment[name] = value
            else:
                fn = eval(expr[0], environment)
                args = [eval(arg, environment) for arg in expr[1:]]
                return apply(fn, args, environment)


def apply(fn: Any, args: List[Any], environment: Dict[str, Any]):
    if callable(fn):
        return fn(*args)

    if isinstance(fn, Lambda):
        new_env = dict(environment)
        if len(args) != len(fn.arguments):
            fail("Mismatched number of arguments to lambda")

        for i in range(len(fn.arguments)):
            new_env[fn.arguments[i].value] = args[i]

        return eval(fn.code, new_env)


base_environment = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    ">": operator.gt,
    ">=": operator.ge,
    "<": operator.lt,
    "<=": operator.le,
    "=": operator.eq,
    "!=": operator.ne,
    "nil": None,
    'print': lambda x: sys.stdout.write(str(x) + '\n')
}


def main():
    if(len(sys.argv)) != 2:
        print(f"usage: python {sys.argv[0]} <file>")
        sys.exit(-1)

    with open(sys.argv[1]) as fd:
        contents = fd.read()
        parsed = parse(tokenize(contents))
        print('Executing...')
        eval(parsed, base_environment)
        print('End state:')
        pp(base_environment)


if __name__ == '__main__':
    main()
