from enum import Enum

class TokenType(Enum):
    TAB = 0
    SPACE = 1
    LINEFEED = 2
    EOF = 3

    @classmethod
    def fromString(self, s: str):
        if s == ' ' or '[Space]':
            return TokenType.SPACE
        elif s == '\t' or '[Tab]':
            return TokenType.TAB
        elif s == '\n' or '[LF]':
            return TokenType.LINEFEED
        else:
            return None


class Token():
    def __init__(self, type: TokenType, line: int):
        self.type = type
        self.line = line

class Tokenizer():
    def __init__(self, text: str):
        self.text = text
        self.index = 0
        self.line = 1
        self.readable_mode = text.count("[") > 0

    def returnNextToken(self):
        self.index += 1
        return self.nextToken()
    
    def nextToken(self) -> Token:
        if self.index >= len(self.text):
            return Token(TokenType.EOF, self.line)
        if self.readable_mode:
            if self.text[self.index] == '[':
                end_index = self.text.index("]", self.index)
                type = TokenType.fromString(self.text[self.index:end_index+1])
                if type == None:
                    return self.returnNextToken()
                self.index = end_index + 1
                return Token(type, self.line)
            elif self.text[self.index] == "\n":
                self.line += 1
                return self.returnNextToken()
            else:
                return self.returnNextToken()
        else:
            if self.text[self.index] in [' ', '\t', '\n']:
                type = TokenType.fromString(self.text[self.index])
                self.index += 1
                if self.text[self.index] == '\n':
                    self.line += 1
                if type == None:
                    return self.nextToken()
                else:
                    return Token(type, self.line - 1)
    
    def allTokens(self) -> list[Token]:
        out = []
        while True:
            tok = self.nextToken()
            if tok.type == TokenType.EOF:
                return out
            else:
                out.append(tok)




def main():
    with open("text.txt", mode="r") as f:
        source = f.read()
    


if __name__ == "__main__":
    main()
