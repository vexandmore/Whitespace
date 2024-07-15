from enum import Enum


class TokenType(Enum):
    TAB = 0
    SPACE = 1
    LINEFEED = 2
    EOF = 3

    @classmethod
    def fromString(self, s: str):
        if s == ' ' or s == '[Space]':
            return TokenType.SPACE
        elif s == '\t' or s == '[Tab]':
            return TokenType.TAB
        elif s == '\n' or s == '[LF]':
            return TokenType.LINEFEED
        else:
            return None


class Token():
    def __init__(self, type: TokenType, line: int):
        self.type = type
        self.line = line
    
    def __eq__(self, value: object) -> bool:
        if type(value) != Token:
            return False
        return self.type == value.type and self.line == value.line
    
    def __repr__(self) -> str:
        return f"Token {self.type} at {self.line}"


# In this context, a BasicToken is space, tab, or linefeed
class Tokenizer():
    def __init__(self, text: str, detect_readable: bool):
        self.text = text
        self.index = 0
        self.line = 1
        if detect_readable:
            self.readable_mode = text.count("[Space]") > 0 and text.count("[Tab]") > 0 and text.count("[LF]") > 0
        else:
            self.readable_mode = False

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
            lexeme = self.text[self.index]

            if lexeme in [' ', '\t', '\n']:
                type = TokenType.fromString(lexeme)
                self.index += 1
                if lexeme == '\n':
                    self.line += 1
                    return Token(type, self.line - 1)
                if type == None:
                    return self.returnNextToken()
                return Token(type, self.line)
            else:
                return self.returnNextToken()
    
    def allTokens(self) -> list[Token]:
        out: list[Token] = []
        while True:
            tok = self.nextToken()
            if tok.type == TokenType.EOF:
                return out
            else:
                out.append(tok)
