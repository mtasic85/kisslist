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
        linenum = 0
        colnum = 0

        while i < len(text):
            c = text[i]

            if c in ('\n', '\r'):
                token = Token(Symbol.NEWLINE, text[i:i + 1], linenum, colnum)
                tokens.append(token)
                linenum += 1
                colnum = 0
                i += 1
            elif c in '_' + string.ascii_letters:
                j = i

                while c in '_' + string.ascii_letters + string.digits:
                    j += 1
                    c = text[j]

                token = Token(Symbol.NAME, text[i:j], linenum, colnum)
                tokens.append(token)
                colnum += j - i
                i = j
            elif c in string.digits:
                # FIXME: possible issue if something invalid is just behind number
                if text[i + 1] == 'x':
                    # hex
                    j = i + 2
                    c = text[j]

                    while c in string.hexdigits:
                        j += 1
                        c = text[j]
                elif text[i + 1] == 'o':
                    # octal
                    j = i + 2
                    c = text[j]

                    while c in '01234567':
                        j += 1
                        c = text[j]
                elif text[i + 1] == 'o':
                    # binary
                    j = i + 2
                    c = text[j]

                    while c in '01234567':
                        j += 1
                        c = text[j]

                token = Token(Symbol.NAME, text[i:j], linenum, colnum)
                tokens.append(token)
                colnum += j - i
                i = j
            else:
                colnum += 1
                i += 1

        return tokens


if __name__ == '__main__':
    text = '''
    _aaa aaa a_a_
    122 __a
    '''

    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(text)
    print('tokens:', tokens)
