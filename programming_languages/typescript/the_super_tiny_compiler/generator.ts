import { ASTNodeType } from './parser';
import { TransformedASTNode } from './transformer';

const codeGenerator = (transformedAST: TransformedASTNode): string => {
  switch (transformedAST.type) {
  case ASTNodeType.Program:
    if (transformedAST.children)
      return transformedAST.children.map(codeGenerator).join('\n');
    break;
  case ASTNodeType.Statement:
    if (transformedAST.children)
      return codeGenerator(transformedAST.children[0]) + ';';
    break;
  case ASTNodeType.CallExpression:
    if (transformedAST.callee)
      return (
        codeGenerator(transformedAST.callee) +
          '(' +
          transformedAST.children?.map(codeGenerator).join(', ') +
          ')'
      );
    break;
  case ASTNodeType.Identifier:
  case ASTNodeType.NumberLiteral:
    if (transformedAST.value) return transformedAST.value;
    break;
  case ASTNodeType.StringLiteral:
    if (transformedAST.value) return '"' + transformedAST.value + '"';
    break;
  default:
    throw new TypeError(transformedAST.type);
  }
  throw new SyntaxError(transformedAST.toString());
};

export { codeGenerator };
