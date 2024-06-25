from whitespace.tokenizer import Tokenizer, TokenType
from whitespace.commands import Command, End, Push, OutChar, OutNum, ReadChar, ReadNum


class Parser(Tokenizer):
    def __init__(self, text: str):
        super().__init__(text)


    def allCommands(self) -> list[Command]:
        out: list[Command] = []
        c = self.nextCommand()
        while c is not None:
            out.append(c)
            c = self.nextCommand()
        return out


    def nextCommand(self) -> Command | None:
        lookahead = self.nextToken()
        if lookahead.type == TokenType.SPACE:
            return self.parseStackManip()
        elif lookahead.type == TokenType.LINEFEED:
            return self.parseFlowControl()
        elif lookahead.type == TokenType.TAB:
            lookahead = self.nextToken()
            if lookahead.type == TokenType.SPACE:
                return self.parseArith()
            elif lookahead.type == TokenType.LINEFEED:
                return self.parseIO()
            elif lookahead.type == TokenType.TAB:
                return self.parseHeap()
            else:
                return None
        else:
            return None
                    
        
    def parseStackManip(self) -> Command | None:
        lookahead = self.nextToken()
        if lookahead.type == TokenType.SPACE:
            return Push(lookahead.line, self.parseNumber())
        else:
            return None
    

    def parseNumber(self) -> int:
        lookahead = self.nextToken()
        out: int = 0

        # A number starts with a sign; Space is 0, tab 1
        if lookahead.type == TokenType.SPACE:
            sign = 1
        elif lookahead.type == TokenType.TAB:
            sign = -1
        else:
            return -1
        lookahead = self.nextToken()

        # For the rest of the number, space is 0, tab is 1 (ends on LF)
        while lookahead.type == TokenType.SPACE or lookahead.type == TokenType.TAB:
            if lookahead.type == TokenType.SPACE:
                # Add 0 to number
                out = out << 1
            elif lookahead.type == TokenType.TAB:
                # Add 1 to number
                out = out << 1
                out += 1

            lookahead = self.nextToken()
        out *= sign

        return out
    

    def parseFlowControl(self) -> Command | None:
        lookahead = self.nextToken()

        if lookahead.type == TokenType.LINEFEED:
            lookahead = self.nextToken()

            if lookahead.type == TokenType.LINEFEED:
                return End(lookahead.line)
            else:
                return None
        else:
            return None
    

    def parseIO(self) -> Command | None:
        lookahead = self.nextToken()

        if lookahead.type == TokenType.SPACE:
            lookahead = self.nextToken()

            if lookahead.type == TokenType.SPACE:
                return OutChar(lookahead.line)
            elif lookahead.type == TokenType.TAB:
                return OutNum(lookahead.line)
            else:
                return None
        elif lookahead.type == TokenType.TAB:
            lookahead = self.nextToken()

            if lookahead.type == TokenType.SPACE:
                return ReadChar(lookahead.line)
            elif lookahead.type == TokenType.TAB:
                return ReadNum(lookahead.line)
            else:
                return None
        else:
            return None
    

    def parseArith(self) -> Command:
        return End(1)
    

    def parseHeap(self) -> Command:
        return End(1)
