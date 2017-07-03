import functools

from parser import Symbol


class Env:
    def __init__(self, *envs):
        self.envs = envs


    def __getitem__(self, key):
        for env in self.envs:
            try:
                return env[key]
            except KeyError as e:
                continue
        else:
            raise KeyError(f'Missing variable "{key}"')


    def __setitem__(self, key, value):
        env = self.envs[-1]
        env[key] = value


    def __contains__(self, key):
        for env in self.envs:
            try:
                value = env[key]
                return True
            except KeyError as e:
                continue
        else:
            return False


class Function:
    def __init__(self, executor, name, params, body, closure):
        self.executor = executor
        self.name = name
        self.params = params
        self.body = body
        self.closure = closure


    def __call__(self, *args):
        globals_ = self.closure
        locals_ = {k: v for k, v in zip(self.params, args)}

        for n in self.body:
            res = self.executor.eval(n, globals_, locals_)

        return res


class Executor:
    def __init__(self, parser):
        self.parser = parser

        def add_(a, b):
            return a + b

        def sub_(a, b):
            return a - b

        def mul_(a, b):
            return a * b

        def div_(a, b):
            return a / b

        def mod_(a, b):
            return a % b

        def pow_(a, b):
            return a ** b

        def not_(a):
            return not a

        def and_(a, b):
            return a and b

        def or_(a, b):
            return a or b
        
        def lt_(a, b):
            return a < b

        def le_(a, b):
            return a <= b

        def gt_(a, b):
            return a > b

        def ge_(a, b):
            return a >= b

        def eq_(a, b):
            return a == b

        def ne_(a, b):
            return a != b

        def print_(*args):
            print(*args)

        def range_(*args):
            return list(range(*args))

        def map_(obj, func):
            return list(map(func, obj))

        def filter_(obj, func):
            return list(filter(func, obj))

        def reduce_(obj, s, func):
            return functools.reduce(func, obj, s)

        def get_(obj, index_or_key):
            return obj[index_or_key]
        
        self.globals = {
            '+': add_,
            '-': sub_,
            '*': mul_,
            '/': div_,
            '%': mod_,
            '**': pow_,
            'not': not_,    '!': not_,
            'and': and_,    '&&': and_,
            'or': or_,      '||': or_,
            '<': lt_,
            '<=': le_,
            '>': gt_,
            '>=': ge_,
            '==': eq_,
            '!=': ne_,
            'print': print_,
            'range': range_,
            'map': map_,
            'filter': filter_,
            'reduce': reduce_,
            'get': get_,
        }


    def exec(self, text, globals_=None, locals_=None):
        tokens = self.parser.tokenizer.tokenize(text)
        # print(f'debug exec tokens: {tokens!r}')
        ast = self.parser.parse(tokens)
        # print(f'debug exec ast: {ast!r}')
        globals_ = globals_ if globals_ else self.globals
        locals_ = locals_ if locals_ else {}

        for n in ast:
            result = self.eval(n, globals_, locals_)

        return result


    def eval(self, ast, globals_, locals_):
        env = Env(globals_, locals_)

        if isinstance(ast, Symbol):
            # variable reference
            return env[ast]
        elif isinstance(ast, (int, float)):
            # number
            return ast
        elif isinstance(ast, list) and ast[0] in ('if', '?'):
            # conditional
            test, conseq, alt = ast[1:]
            test_result = self.eval(test, globals_, locals_)
            # print('test_result:', test_result)

            if test_result:
                for n in conseq:
                    # print('n[0]:', n)
                    res = self.eval(n, globals_, locals_)
                    # print('res[0]:', res)
            else:
                for n in alt:
                    res = self.eval(n, globals_, locals_)
                    # print('res[1]:', res)
            
            return res
        elif isinstance(ast, list) and ast[0] == 'def':
            # variable
            var, exp = ast[1:]
            res = self.eval(exp, globals_, locals_)
            env[var] = res
            return res
        elif isinstance(ast, list) and ast[0] == 'fn':
            # function
            # print('!2')
            name, params, body = ast[1:]
            func = Function(self, name, params, body, env)
            env[name] = func
            return func
        elif isinstance(ast, list) and ast[0] == 'lambda':
            # function
            # print('!2')
            params, body = ast[1:]
            func = Function(self, None, params, body, env)
            return func
        elif isinstance(ast, list) and ast[0] in env and callable(env[ast[0]]):
            # function call
            func = self.eval(ast[0], globals_, locals_)
            args = [self.eval(arg, globals_, locals_) for arg in ast[1:]]
            res = func(*args)
            return res
        else:
            # constant literal
            return ast
