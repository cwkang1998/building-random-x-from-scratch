const WHITESPACE = /\s/;
const LETTERS = /[a-z]/i;
const NUMBERS = /[0-9]/;

type Token = {
  type: string;
  value: string;
};

const tokenizer = (input: string): Array<Token> => {
  let current = 0;
  const tokens: Array<Token> = [];

  while (current < input.length) {
    let char: string = input[current];

    // Check to see what token it is
    if (char === '(' || char === ')') {
      // Parenthesis token
      tokens.push({
        type: 'paren',
        value: char,
      });
      current++;
    } else if (WHITESPACE.test(char)) {
      // Whitespace would be skipped
      current++;
    } else if (NUMBERS.test(char)) {
      // Number token
      let value = '';

      while (NUMBERS.test(char)) {
        value += char;
        char = input[++current];
      }

      tokens.push({
        type: 'number',
        value,
      });
    } else if (char === '"') {
      // String token, check for quotes
      let value = '';

      // Skip the starting quote
      char = input[++current];

      while (char !== '"') {
        value += char;
        char = input[++current];
      }

      // Skip the ending quote
      char = input[++current];

      tokens.push({
        type: 'string',
        value,
      });
    } else if (LETTERS.test(char)) {
      let value = '';

      while (LETTERS.test(char)) {
        value += char;
        char = input[++current];
      }

      tokens.push({
        type: 'name',
        value,
      });
    } else {
      throw new TypeError(`Unknown character ${char}.`);
    }
  }

  return tokens;
};

export { Token, tokenizer };
