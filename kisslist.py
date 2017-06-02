import os
import sys

from tokenizer import Tokenizer
from parser import Parser
from executor import Executor

if __name__ == '__main__':
    path = sys.argv[-1]

    with open(path, 'r') as f:
        text = f.read()

    tokenizer = Tokenizer()
    parser = Parser(tokenizer)
    executor = Executor(parser)
    result = executor.exec(text)
