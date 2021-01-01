import { ASTNode, ASTNodeType } from './parser';

type BaseTransformedASTNode = {
  type: ASTNodeType;
  value: string | null;
};

type TransformedASTNode = BaseTransformedASTNode & {
  callee?: BaseTransformedASTNode | null;
  children?: Array<BaseTransformedASTNode | TransformedASTNode>;
};

const transformer = (ast: ASTNode): TransformedASTNode => {
  const traverse = (
    oriAST: ASTNode,
    parent: ASTNode | null = null
  ): TransformedASTNode => {
    let node: TransformedASTNode = {
      type: ASTNodeType.Program,
      value: null,
      callee: null,
      children: new Array<BaseTransformedASTNode | TransformedASTNode>(),
    };
    switch (oriAST.type) {
    case ASTNodeType.Program:
      node = {
        type: ASTNodeType.Program,
        value: null,
        callee: null,
        children: new Array<BaseTransformedASTNode | TransformedASTNode>(),
      };
      node.children = oriAST.children.map((child) => traverse(child, oriAST));
      break;
    case ASTNodeType.CallExpression: {
      const expression: TransformedASTNode = {
        type: ASTNodeType.CallExpression,
        value: null,
        callee: {
          type: ASTNodeType.Identifier,
          value: oriAST.value,
        },
        children: new Array<BaseTransformedASTNode | TransformedASTNode>(),
      };

      expression.children = oriAST.children.map((child) =>
        traverse(child, oriAST)
      );

      if (parent?.type !== ASTNodeType.CallExpression) {
        node = {
          type: ASTNodeType.Statement,
          value: null,
          callee: null,
          children: new Array<BaseTransformedASTNode | TransformedASTNode>(),
        };
        node.children?.push(expression);
      } else {
        node = expression;
      }
      break;
    }
    case ASTNodeType.NumberLiteral:
      node = {
        type: ASTNodeType.NumberLiteral,
        value: oriAST.value,
        callee: null,
        children: new Array<BaseTransformedASTNode | TransformedASTNode>(),
      };
      break;
    case ASTNodeType.StringLiteral:
      node = {
        type: ASTNodeType.StringLiteral,
        value: oriAST.value,
        callee: null,
        children: new Array<BaseTransformedASTNode | TransformedASTNode>(),
      };
      break;
    default:
      throw new TypeError('Unknown type.');
    }

    return node;
  };

  return traverse(ast);
};
export { BaseTransformedASTNode, TransformedASTNode, transformer };
