import sys


class Symbol(str):
    pass


class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer


    def parse(self, tokens):
        ast = []
        i = 0

        while i < len(tokens):
            i, sub_ast = self._parse(i, tokens)
            ast.append(sub_ast)

        return ast


    def _parse(self, i, tokens):
        while i < len(tokens):
            token = tokens[i]
            
            if token == '(':
                ast = []
                i += 1

                while tokens[i] != ')':
                    new_i, sub_ast = self._parse(i, tokens)
                    ast.append(sub_ast)
                    i = new_i

                return i + 1, ast
            elif token != ')':
                ast = self.atom(token)
                return i + 1, ast
            else:
                raise SyntaxError('Unexpected ")"')


    def atom(self, token):
        if token == 'true':
            return True
        elif token == 'false':
            return False
        elif token in ('nil', 'null'):
            return None
        else:
            try:
                return int(token)
            except ValueError:
                try:
                    return float(token)
                except ValueError:
                    return Symbol(token)
