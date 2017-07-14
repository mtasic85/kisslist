from tokenizer import Symbol

class Ast:
    pass

class SuiteAst(Ast):
    def __init__(self, expr_list):
        self.expr_list = expr_list

class ExprListAst(Ast):
    def __init__(self, exprs):
        self.exprs = exprs

class ExprAst(Ast):
    def __init__(self, expr_stmt):
        self.expr_stmt = expr_stmt



class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.tokens = None
        self.token_index = 0
        self.token = None


    def parse(self):
        self.tokens = self.tokenizer.tokenize()
        self.token_index = 0
        self.token = self.tokens[self.token_index]


    def next_token(self):
        self.token_index += 1
        self.token = self.tokens[self.token_index]
        return self.token

    
    def error(self, msg):
        print(f'Syntax Error: {msg}')


    def accept(self, s):
        if self.token.symbol == s:
            self.next_token()
            return True

        return False


    def expect(self, s):
        if self.accept(s):
            return True

        self.error('invalid syntax')
        return True

    
    def parse_suite(self):
        self.expect(Symbol.LBRACE)
        stmtlist = self.parse_expr_list()
        self.expect(Symbol.RBRACE)

        ast = SuiteAst(expr_list=expr_list)
        return ast


    def parse_expr_list(self):
        exprs = []

        # '}' closes `suite`
        while self.token.symbol != Symbol.RBRACE:
            self.accept()

        ast = ExprListAst(exprs)
        return ast