import { tokenizer } from './tokenizer';
import { parser } from './parser';
import { transformer } from './transformer';
import { codeGenerator } from './generator';

const testProgram = `
(add (substract 10 20) 30)
`;

const token = tokenizer(testProgram);
const ast = parser(token);
const newAst = transformer(ast);
const code = codeGenerator(newAst);
console.log(code);
