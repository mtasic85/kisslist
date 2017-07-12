import string
from enum import Enum, auto

class Symbol(Enum):
    ERRORTOKEN = auto()
    BEGINMARKER = auto()
    ENDMARKER = auto()
    NEWLINE = auto()
    NAME = auto()
    NUMBER = auto()
    STRING = auto()
    LPAR = auto()
    RPAR = auto()
    LSQB = auto()
    RSQB = auto()
    LBRACE = auto()
    RBRACE = auto()
    COLON = auto()
    COMMA = auto()
    SEMI = auto()
    QUESTIONMARK = auto()
    EXCLAMATIONMARK = auto()
    AT = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    VBAR = auto()
    AMPER = auto()
    LESS = auto()
    GREATER = auto()
    EQUAL = auto()
    DOT = auto()
    PERCENT = auto()
    TILDE = auto()
    CIRCUMFLEX = auto()
    EQEQUAL = auto()
    NOTEQUAL = auto()
    LESSEQUAL = auto()
    GREATEREQUAL = auto()
    LEFTSHIFT = auto()
    RIGHTSHIFT = auto()
    DOUBLESTAR = auto()
    PLUSEQUAL = auto()
    MINEQUAL = auto()
    STAREQUAL = auto()
    SLASHEQUAL = auto()
    PERCENTEQUAL = auto()
    VBAREQUAL = auto()
    AMPEREQUAL = auto()
    CIRCUMFLEXEQUAL = auto()
    LEFTSHIFTEQUAL = auto()
    RIGHTSHIFTEQUAL = auto()
    DOUBLESTAREQUAL = auto()
    DOUBLEAMPER = auto()
    DOUBLEVBAR = auto()
    ARROW = auto()

class Token:
    def __init__(self, symbol, text, linenum, colnum):
        self.symbol = symbol
        self.text = text
        self.linenum = linenum
        self.colnum = colnum


    def __repr__(self):
        return f'<{self.__class__.__name__} {self.symbol} {self.text!r} {self.linenum} {self.colnum}>'


class Tokenizer:
    def __init__(self):
        pass

    def tokenize(self, text):
        tokens = []
        i = 0
        linenum = 1
        colnum = 1

        token = Token(Symbol.BEGINMARKER, text[0:0], linenum, colnum)
        tokens.append(token)

        while i < len(text):
            c = text[i]

            if c in ('\n', '\r'):
                # new line
                token = Token(Symbol.NEWLINE, text[i:i + 1], linenum, colnum)
                tokens.append(token)
                linenum += 1
                colnum = 1
                i += 1
            elif c in '_' + string.ascii_letters:
                # name
                j = i

                while c in '_' + string.ascii_letters + string.digits:
                    j += 1
                    c = text[j]

                token = Token(Symbol.NAME, text[i:j], linenum, colnum)
                tokens.append(token)
                colnum += j - i
                i = j
            elif c in string.digits:
                # number
                if text[i + 1] == 'x':
                    # hex
                    j = i + 2
                    c = text[j]

                    while True:
                        if c in string.hexdigits:
                            j += 1
                            c = text[j]
                        elif c in '!"$%&\'()*+,-./:;<=>?@[\\]^`{|}~ \t\n\r\x0b\x0c':
                            token = Token(Symbol.NUMBER, text[i:j], linenum, colnum)
                            break
                        else:
                            token = Token(Symbol.ERRORTOKEN, text[i:j], linenum, colnum)
                            break

                    tokens.append(token)
                    colnum += j - i
                    i = j
                elif text[i + 1] == 'o':
                    # octal
                    j = i + 2
                    c = text[j]

                    while True:
                        if c in string.octdigits:
                            j += 1
                            c = text[j]
                        elif c in '!"$%&\'()*+,-./:;<=>?@[\\]^`{|}~ \t\n\r\x0b\x0c':
                            token = Token(Symbol.NUMBER, text[i:j], linenum, colnum)
                            break
                        else:
                            token = Token(Symbol.ERRORTOKEN, text[i:j], linenum, colnum)
                            break

                    tokens.append(token)
                    colnum += j - i
                    i = j
                elif text[i + 1] == 'b':
                    # binary
                    j = i + 2
                    c = text[j]

                    while True:
                        if c in '01':
                            j += 1
                            c = text[j]
                        elif c in '!"$%&\'()*+,-./:;<=>?@[\\]^`{|}~ \t\n\r\x0b\x0c':
                            token = Token(Symbol.NUMBER, text[i:j], linenum, colnum)
                            break
                        else:
                            token = Token(Symbol.ERRORTOKEN, text[i:j], linenum, colnum)
                            break

                    tokens.append(token)
                    colnum += j - i
                    i = j
                elif text[i + 1] in string.digits:
                    # decimal
                    j = i + 1
                    c = text[j]

                    while True:
                        if c in string.digits:
                            j += 1
                            c = text[j]
                        elif c in '!"$%&\'()*+,-./:;<=>?@[\\]^`{|}~ \t\n\r\x0b\x0c':
                            token = Token(Symbol.NUMBER, text[i:j], linenum, colnum)
                            break
                        else:
                            token = Token(Symbol.ERRORTOKEN, text[i:j], linenum, colnum)
                            break

                    tokens.append(token)
                    colnum += j - i
                    i = j
                elif text[i + 1] in '!"$%&\'()*+,-./:;<=>?@[\\]^`{|}~ \t\n\r\x0b\x0c':
                    token = Token(Symbol.NUMBER, text[i:i + 1], linenum, colnum)
                    tokens.append(token)
                    colnum += 1
                    i += 1
                else:
                    token = Token(Symbol.ERRORTOKEN, text[i:i + 1], linenum, colnum)
                    tokens.append(token)
                    colnum += 1
                    i += 1
            elif c == '\'':
                # ' string
                j = i + 1
                c = text[j]

                while c is not '\'':
                    if c == '\\':
                        j += 2
                    else:
                        j += 1

                    if j >= len(text):
                        break

                    c = text[j]

                if c == '\'':
                    j += 1
                    token = Token(Symbol.STRING, text[i:j], linenum, colnum)
                    tokens.append(token)
                else:
                    token = Token(Symbol.ERRORTOKEN, text[i:j], linenum, colnum)
                    tokens.append(token)
                
                colnum += j - i
                i = j
            elif c == '(':
                token = Token(Symbol.LPAR, text[i:i + 1], linenum, colnum)
                tokens.append(token)
                colnum += 1
                i += 1
            elif c == ')':
                token = Token(Symbol.RPAR, text[i:i + 1], linenum, colnum)
                tokens.append(token)
                colnum += 1
                i += 1
            elif c == '[':
                token = Token(Symbol.LSQB, text[i:i + 1], linenum, colnum)
                tokens.append(token)
                colnum += 1
                i += 1
            elif c == ']':
                token = Token(Symbol.RSQB, text[i:i + 1], linenum, colnum)
                tokens.append(token)
                colnum += 1
                i += 1
            elif c == '{':
                token = Token(Symbol.LBRACE, text[i:i + 1], linenum, colnum)
                tokens.append(token)
                colnum += 1
                i += 1
            elif c == '}':
                token = Token(Symbol.RBRACE, text[i:i + 1], linenum, colnum)
                tokens.append(token)
                colnum += 1
                i += 1
            elif c == ':':
                token = Token(Symbol.COLON, text[i:i + 1], linenum, colnum)
                tokens.append(token)
                colnum += 1
                i += 1
            elif c == ';':
                token = Token(Symbol.SEMI, text[i:i + 1], linenum, colnum)
                tokens.append(token)
                colnum += 1
                i += 1
            elif c == '.':
                token = Token(Symbol.DOT, text[i:i + 1], linenum, colnum)
                tokens.append(token)
                colnum += 1
                i += 1
            elif c == ',':
                token = Token(Symbol.COMMA, text[i:i + 1], linenum, colnum)
                tokens.append(token)
                colnum += 1
                i += 1
            elif c == '?':
                token = Token(Symbol.QUESTIONMARK, text[i:i + 1], linenum, colnum)
                tokens.append(token)
                colnum += 1
                i += 1
            elif c == '@':
                token = Token(Symbol.AT, text[i:i + 1], linenum, colnum)
                tokens.append(token)
                colnum += 1
                i += 1
            elif c == '~':
                token = Token(Symbol.TILDE, text[i:i + 1], linenum, colnum)
                tokens.append(token)
                colnum += 1
                i += 1
            elif c == '+':
                if text[i + 1] == '=':
                    token = Token(Symbol.PLUSEQUAL, text[i:i + 2], linenum, colnum)
                    tokens.append(token)
                    colnum += 2
                    i += 2
                else:
                    token = Token(Symbol.PLUS, text[i:i + 1], linenum, colnum)
                    tokens.append(token)
                    colnum += 1
                    i += 1
            elif c == '-':
                if text[i + 1] == '=':
                    token = Token(Symbol.MINEQUAL, text[i:i + 2], linenum, colnum)
                    tokens.append(token)
                    colnum += 2
                    i += 2
                else:
                    token = Token(Symbol.MINUS, text[i:i + 1], linenum, colnum)
                    tokens.append(token)
                    colnum += 1
                    i += 1
            elif c == '*':
                if text[i + 1] == '=':
                    token = Token(Symbol.STAREQUAL, text[i:i + 2], linenum, colnum)
                    tokens.append(token)
                    colnum += 2
                    i += 2
                elif text[i + 1] == '*':
                    if text[i + 2] == '=':
                        token = Token(Symbol.DOUBLESTAREQUAL, text[i:i + 3], linenum, colnum)
                        tokens.append(token)
                        colnum += 3
                        i += 3
                    else:
                        token = Token(Symbol.DOUBLESTAR, text[i:i + 2], linenum, colnum)
                        tokens.append(token)
                        colnum += 2
                        i += 2
                else:
                    token = Token(Symbol.STAR, text[i:i + 1], linenum, colnum)
                    tokens.append(token)
                    colnum += 1
                    i += 1
            elif c == '/':
                if text[i + 1] == '=':
                    token = Token(Symbol.SLASHEQUAL, text[i:i + 2], linenum, colnum)
                    tokens.append(token)
                    colnum += 2
                    i += 2
                else:
                    token = Token(Symbol.SLASH, text[i:i + 1], linenum, colnum)
                    tokens.append(token)
                    colnum += 1
                    i += 1
            elif c == '|':
                if text[i + 1] == '=':
                    token = Token(Symbol.VBAREQUAL, text[i:i + 2], linenum, colnum)
                    tokens.append(token)
                    colnum += 2
                    i += 2
                elif text[i + 1] == '|':
                    token = Token(Symbol.DOUBLEVBAR, text[i:i + 2], linenum, colnum)
                    tokens.append(token)
                    colnum += 2
                    i += 2
                else:
                    token = Token(Symbol.VBAR, text[i:i + 1], linenum, colnum)
                    tokens.append(token)
                    colnum += 1
                    i += 1
            elif c == '&':
                if text[i + 1] == '=':
                    token = Token(Symbol.AMPEREQUAL, text[i:i + 2], linenum, colnum)
                    tokens.append(token)
                    colnum += 2
                    i += 2
                elif text[i + 1] == '&':
                    token = Token(Symbol.DOUBLEAMPER, text[i:i + 2], linenum, colnum)
                    tokens.append(token)
                    colnum += 2
                    i += 2
                else:
                    token = Token(Symbol.AMPER, text[i:i + 1], linenum, colnum)
                    tokens.append(token)
                    colnum += 1
                    i += 1
            elif c == '%':
                if text[i + 1] == '=':
                    token = Token(Symbol.PERCENTEQUAL, text[i:i + 2], linenum, colnum)
                    tokens.append(token)
                    colnum += 2
                    i += 2
                else:
                    token = Token(Symbol.PERCENT, text[i:i + 1], linenum, colnum)
                    tokens.append(token)
                    colnum += 1
                    i += 1
            elif c == '^':
                if text[i + 1] == '=':
                    token = Token(Symbol.CIRCUMFLEXEQUAL, text[i:i + 2], linenum, colnum)
                    tokens.append(token)
                    colnum += 2
                    i += 2
                else:
                    token = Token(Symbol.CIRCUMFLEX, text[i:i + 1], linenum, colnum)
                    tokens.append(token)
                    colnum += 1
                    i += 1
            elif c == '=':
                if text[i + 1] == '=':
                    token = Token(Symbol.EQEQUAL, text[i:i + 2], linenum, colnum)
                    tokens.append(token)
                    colnum += 2
                    i += 2
                else:
                    token = Token(Symbol.EQUAL, text[i:i + 1], linenum, colnum)
                    tokens.append(token)
                    colnum += 1
                    i += 1
            elif c == '!':
                if text[i + 1] == '=':
                    token = Token(Symbol.NOTEQUAL, text[i:i + 2], linenum, colnum)
                    tokens.append(token)
                    colnum += 2
                    i += 2
                else:
                    token = Token(Symbol.EXCLAMATIONMARK, text[i:i + 1], linenum, colnum)
                    tokens.append(token)
                    colnum += 1
                    i += 1
            elif c == '<':
                if text[i + 1] == '=':
                    token = Token(Symbol.LESSEQUAL, text[i:i + 2], linenum, colnum)
                    tokens.append(token)
                    colnum += 2
                    i += 2
                elif text[i + 1] == '<':
                    if text[i + 2] == '=':
                        token = Token(Symbol.LEFTSHIFTEQUAL, text[i:i + 3], linenum, colnum)
                        tokens.append(token)
                        colnum += 3
                        i += 3
                    else:
                        token = Token(Symbol.LEFTSHIFT, text[i:i + 2], linenum, colnum)
                        tokens.append(token)
                        colnum += 2
                        i += 2
                else:
                    token = Token(Symbol.LESS, text[i:i + 1], linenum, colnum)
                    tokens.append(token)
                    colnum += 1
                    i += 1
            elif c == '>':
                if text[i + 1] == '=':
                    token = Token(Symbol.GREATEREQUAL, text[i:i + 2], linenum, colnum)
                    tokens.append(token)
                    colnum += 2
                    i += 2
                elif text[i + 1] == '>':
                    if text[i + 2] == '=':
                        token = Token(Symbol.RIGHTSHIFTEQUAL, text[i:i + 3], linenum, colnum)
                        tokens.append(token)
                        colnum += 3
                        i += 3
                    else:
                        token = Token(Symbol.RIGHTSHIFT, text[i:i + 2], linenum, colnum)
                        tokens.append(token)
                        colnum += 2
                        i += 2
                else:
                    token = Token(Symbol.GREATER, text[i:i + 1], linenum, colnum)
                    tokens.append(token)
                    colnum += 1
                    i += 1
            elif c in string.whitespace:
                colnum += 1
                i += 1
            else:
                token = Token(Symbol.ERRORTOKEN, text[i:i + 1], linenum, colnum)
                tokens.append(token)
                colnum += 1
                i += 1

        token = Token(Symbol.ENDMARKER, text[-1:-1], linenum, colnum)
        tokens.append(token)
        return tokens


if __name__ == '__main__':
    text = r'''
    _aaa aaa a_a_
    122 __a 0x12f 0x1() 0x1g
    0b111 0o333
    123g 'asasa' 'frfr \' asda'
    () ( ) (1,) (a, 110, 0b1, 0o7)
    [[1], (,)]
    
    '
    '

    f = (x, y) -> {x + y}
    g = (h) -> (x, y) -> f(x, y)
    g(f)(10, 20)
    a += 1
    b-=a
    c*= b
    d /= c
    e <<= d
    f >> e
    g == f
    h != g + !f
    _ '$' = 1
    a ** b
    c **= d
    '''

    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(text)
    print('tokens:')
    for n in tokens: print(n)
