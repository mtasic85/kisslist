import sys

from tokenizer import Tokenizer
from parser import Parser

if __name__ == '__main__':
    path = sys.argv[1]
    tokenizer = Tokenizer(path)
    parser = Parser(tokenizer)
    ast = parser.parse()
    print(ast)