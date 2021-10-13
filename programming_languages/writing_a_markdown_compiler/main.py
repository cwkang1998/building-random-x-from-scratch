from parser import Parser
from tokenizer import Tokenizer
from generator import Generator
tokenizer = Tokenizer()
parser = Parser()
generator = Generator()

tokens = tokenizer.tokenize('**Hello**\n\nwell _whats this_??? WORLD\n')
ast = parser.parse(tokens)
result = generator.generate(ast)
print(result)
