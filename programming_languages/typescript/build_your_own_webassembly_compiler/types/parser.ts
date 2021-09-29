interface Parser {
  (tokens: Token[]): Program;
}

interface ProgramNode {
  type: string;
}

type ExpressionNode = NumberLiteralNode;

type StatementNode = PrintStatementNode;

type Program = StatementNode[];

interface NumberLiteralNode extends ProgramNode {
  type: 'numberLiteral';
  value: number;
}

interface IdentifierNode extends ProgramNode {
  type: 'identifier';
  value: string;
}

interface PrintStatementNode extends ProgramNode {
  type: 'printStatement';
  expression: ExpressionNode;
}

interface ParserStep<T extends ProgramNode> {
  (): T | undefined;
}
