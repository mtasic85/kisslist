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
    AT = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    DOUBLESLASH = auto()
    VBAR = auto()
    AMPER = auto()
    LESS = auto()
    GREATER = auto()
    EQUAL = auto()
    DOT = auto()
    PERCENT = auto()
    EQEQUAL = auto()
    NOTEQUAL = auto()
    LESSEQUAL = auto()
    GREATEREQUAL = auto()
    TILDE = auto()
    CIRCUMFLEX = auto()
    LEFTSHIFT = auto()
    RIGHTSHIFT = auto()
    DOUBLESTAR = auto()
    PLUSEQUAL = auto()
    MINEQUAL = auto()
    STAREQUAL = auto()
    SLASHEQUAL = auto()
    PERCENTEQUAL = auto()
    AMPEREQUAL = auto()
    VBAREQUAL = auto()
    CIRCUMFLEXEQUAL = auto()
    LEFTSHIFTEQUAL = auto()
    RIGHTSHIFTEQUAL = auto()
    DOUBLESTAREQUAL = auto()
    DOUBLESLASHEQUAL = auto()

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
                        if c in '01234567':
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
                # lpar
                token = Token(Symbol.LPAR, text[i:i + 1], linenum, colnum)
                tokens.append(token)
                colnum += 1
                i += 1
            elif c == ')':
                # rpar
                token = Token(Symbol.RPAR, text[i:i + 1], linenum, colnum)
                tokens.append(token)
                colnum += 1
                i += 1
            elif c == '[':
                # lpar
                token = Token(Symbol.LSQB, text[i:i + 1], linenum, colnum)
                tokens.append(token)
                colnum += 1
                i += 1
            elif c == ']':
                # rpar
                token = Token(Symbol.RSQB, text[i:i + 1], linenum, colnum)
                tokens.append(token)
                colnum += 1
                i += 1
            elif c == '{':
                # lpar
                token = Token(Symbol.LBRACE, text[i:i + 1], linenum, colnum)
                tokens.append(token)
                colnum += 1
                i += 1
            elif c == '}':
                # rpar
                token = Token(Symbol.RBRACE, text[i:i + 1], linenum, colnum)
                tokens.append(token)
                colnum += 1
                i += 1
            else:
                colnum += 1
                i += 1

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
    '''

    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(text)
    print('tokens:')
    for n in tokens: print(n)
