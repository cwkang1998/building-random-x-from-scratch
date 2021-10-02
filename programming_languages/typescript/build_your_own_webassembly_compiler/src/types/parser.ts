interface Parser {
  (tokens: Token[]): Program;
}

interface ProgramNode {
  type: string;
}

type Operator = '+' | '-' | '*' | '/' | '==' | '>' | '<' | '&&';

type ExpressionNode = NumberLiteralNode | BinaryExpressionNode | IdentifierNode;

type StatementNode =
  | PrintStatementNode
  | VariableDeclarationNode
  | WhileStatementNode
  | VariableAssignmentNode
  | SetPixelStatementNode;

type Program = StatementNode[];

interface VariableDeclarationNode extends ProgramNode {
  type: 'variableDeclaration';
  name: string;
  initializer: ExpressionNode;
}

interface NumberLiteralNode extends ProgramNode {
  type: 'numberLiteral';
  value: number;
}

interface BinaryExpressionNode extends ProgramNode {
  type: 'binaryExpression';
  left: ExpressionNode;
  right: ExpressionNode;
  operator: Operator;
}

interface VariableAssignmentNode extends ProgramNode {
  type: 'variableAssignment';
  name: string;
  value: ExpressionNode;
}

interface IdentifierNode extends ProgramNode {
  type: 'identifier';
  value: string;
}

interface PrintStatementNode extends ProgramNode {
  type: 'printStatement';
  expression: ExpressionNode;
}
interface WhileStatementNode extends ProgramNode {
  type: 'whileStatement';
  expression: ExpressionNode;
  statements: StatementNode[];
}

interface SetPixelStatementNode extends ProgramNode {
  type: 'setpixelStatement';
  x: ExpressionNode;
  y: ExpressionNode;
  color: ExpressionNode;
}

interface ParserStep<T extends ProgramNode> {
  (): T | undefined;
}
