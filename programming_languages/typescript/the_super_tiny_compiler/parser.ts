import { Token } from './tokenizer';

enum ASTNodeType {
  Program,
  Statement,
  Identifier,
  StringLiteral,
  NumberLiteral,
  CallExpression,
}

type ASTNode = {
  type: ASTNodeType;
  value: string | null;
  children: Array<ASTNode>;
};

const parser = (tokens: Array<Token>): ASTNode => {
  let current = 0;

  const walk = (): ASTNode => {
    let curToken = tokens[current];

    if (curToken.type === 'number') {
      current++;

      return {
        type: ASTNodeType.NumberLiteral,
        value: curToken.value,
        children: new Array<ASTNode>(),
      };
    }
    if (curToken.type === 'string') {
      current++;

      return {
        type: ASTNodeType.StringLiteral,
        value: curToken.value,
        children: new Array<ASTNode>(),
      };
    }
    if (curToken.type === 'paren' && curToken.value === '(') {
      // Skip parenthesis
      curToken = tokens[++current];

      const node = {
        type: ASTNodeType.CallExpression,
        value: curToken.value,
        children: new Array<ASTNode>(),
      };

      // skip name token
      curToken = tokens[++current];

      while (
        curToken.type !== 'paren' ||
        (curToken.type === 'paren' && curToken.value !== ')')
      ) {
        node.children.push(walk());
        curToken = tokens[current];
      }
      current++;

      return node;
    }

    throw new TypeError(curToken.type);
  };

  const ast = {
    type: ASTNodeType.Program,
    value: null,
    children: new Array<ASTNode>(),
  };

  while (current < tokens.length) {
    ast.children.push(walk());
  }
  return ast;
};

export { ASTNode, ASTNodeType, parser };
