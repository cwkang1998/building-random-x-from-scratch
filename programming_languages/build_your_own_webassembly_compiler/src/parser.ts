export class ParserError extends Error {
  token: Token;
  constructor(message: string, token: Token) {
    super(message);
    this.token = token;
  }
}

const asOperator = (value: string): Operator => {
  return value as Operator;
};

export const parse: Parser = (tokens) => {
  const tokenIterator = tokens[Symbol.iterator]();
  let currentToken = tokenIterator.next().value;

  const currentTokenIsKeyword = (name: string) =>
    currentToken.value == name && currentToken.type === 'keyword';

  const eatToken = (value?: string) => {
    if (value && value !== currentToken.value) {
      throw new ParserError(
        `Unexpected token value, expected ${value}, received ${currentToken.value}`,
        currentToken
      );
    }
    currentToken = tokenIterator.next().value;
  };

  const parseExpression: ParserStep<ExpressionNode> = () => {
    switch (currentToken.type) {
      case 'number': {
        const node: NumberLiteralNode = {
          type: 'numberLiteral',
          value: Number(currentToken.value),
        };
        eatToken();
        return node;
      }
      case 'identifier': {
        const node: IdentifierNode = {
          type: 'identifier',
          value: currentToken.value,
        };
        eatToken();
        return node;
      }
      case 'parens': {
        eatToken('(');
        const left = parseExpression() as ExpressionNode;
        const operator = currentToken.value;
        eatToken();
        const right = parseExpression() as ExpressionNode;
        eatToken(')');
        return {
          type: 'binaryExpression',
          left,
          right,
          operator: asOperator(operator),
        };
      }

      default:
        throw new ParserError(
          `Unexpected token type ${currentToken.type}`,
          currentToken
        );
    }
  };

  const parsePrintStatement: ParserStep<PrintStatementNode> = () => {
    eatToken('print');
    return {
      type: 'printStatement',
      expression: parseExpression()!,
    };
  };

  const parseVariableDeclarationStatement: ParserStep<VariableDeclarationNode> =
    () => {
      eatToken('var');
      const name = currentToken.value;
      eatToken();
      eatToken('=');
      return {
        type: 'variableDeclaration',
        name,
        initializer: parseExpression()!,
      };
    };

  const parseWhileStatement: ParserStep<WhileStatementNode> = () => {
    eatToken('while');

    const expression = parseExpression();

    const statements: StatementNode[] = [];
    while (!currentTokenIsKeyword('endwhile')) {
      statements.push(parseStatement()!);
    }
    eatToken('endwhile');

    return {
      type: 'whileStatement',
      expression,
      statements,
    } as WhileStatementNode;
  };

  const parseVariableAssignment: ParserStep<VariableAssignmentNode> = () => {
    const name = currentToken.value;
    eatToken();
    eatToken('=');
    return {
      type: 'variableAssignment',
      name,
      value: parseExpression() as ExpressionNode,
    };
  };

  const parseSetPixelStatement: ParserStep<SetPixelStatementNode> = () => {
    eatToken('setpixel');
    return {
      type: 'setpixelStatement',
      x: parseExpression(),
      y: parseExpression(),
      color: parseExpression(),
    } as SetPixelStatementNode;
  };

  const parseStatement: ParserStep<StatementNode> = () => {
    if (currentToken.type === 'keyword') {
      switch (currentToken.value) {
        case 'print':
          return parsePrintStatement();
        case 'var':
          return parseVariableDeclarationStatement();
        case 'while':
          return parseWhileStatement();
        case 'setpixel':
          return parseSetPixelStatement();
        default:
          throw new ParserError(
            `Unknown keyword ${currentToken.value}`,
            currentToken
          );
      }
    } else if (currentToken.type === 'identifier') {
      return parseVariableAssignment();
    }
  };

  const nodes: StatementNode[] = [];
  while (currentToken) {
    nodes.push(parseStatement()!);
  }

  return nodes;
};
