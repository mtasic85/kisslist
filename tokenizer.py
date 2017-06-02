
class Tokenizer:
    def tokenize(self, text):
        # remove comments but keep empty lines instead
        # to preserve line numbers
        lines = text.splitlines()
        lines = [('' if line.strip().startswith(';') else line) for line in lines]
        t = '\n'.join(lines)

        # expand symbols for easier tokenization
        t = t.replace('(', ' ( ')
        t = t.replace(')', ' ) ')
        tokens = t.split()
        return tokens
