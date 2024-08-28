from whitespace.Tokenizer import Tokenizer, TokenType
from whitespace.Commands import Command, End, Push, OutChar, OutNum, ReadChar, ReadNum, Duplicate, Swap, Discard
from whitespace.Commands import Plus, Minus, Times, IntDivide, Modulo
from whitespace.Commands import Read_Heap, Write_Heap
from whitespace.Commands import CallSub, EndSub, Jump, JumpZero, JumpNegative
from whitespace.Commands import Copy, Slide

class Parser(Tokenizer):
    def __init__(self, text: str, detect_readable: bool):
        super().__init__(text, detect_readable)
        self.label = -1

    def get_label(self):
        label = self.label
        # Reset current label so only the next instruction has this label
        self.label = -1
        return label


    def allCommands(self) -> list[Command]:
        out: list[Command] = []
        c = self.nextCommand()
        while c is not None:
            out.append(c)
            c = self.nextCommand()
        return out


    def nextCommand(self) -> Command | None:
        lookahead = self.nextToken()
        if lookahead.type == TokenType.EOF:
            return None

        token = None
        if lookahead.type == TokenType.SPACE:
            token = self.parseStackManip()
        elif lookahead.type == TokenType.LINEFEED:
            token = self.parseFlowControl()
        elif lookahead.type == TokenType.TAB:
            lookahead = self.nextToken()
            if lookahead.type == TokenType.SPACE:
                token = self.parseArith()
            elif lookahead.type == TokenType.LINEFEED:
                token = self.parseIO()
            elif lookahead.type == TokenType.TAB:
                token = self.parseHeap()

        if token == None:
            # In this case, the parse failed somewhere along the way.
            # For now, this is detected here and we raise an error.
            raise Exception(f"Cannot parse command, on line {self.line} index {self.index}")
        else:
            return token
    
        
    def parseStackManip(self) -> Command | None:
        lookahead = self.nextToken()
        if lookahead.type == TokenType.SPACE:
            return Push(lookahead.line, self.parseNumber(), self.get_label())
        elif lookahead.type == TokenType.LINEFEED:
            lookahead = self.nextToken()
            if lookahead.type == TokenType.SPACE:
                return Duplicate(lookahead.line, self.get_label())
            elif lookahead.type == TokenType.TAB:
                return Swap(lookahead.line, self.get_label())
            elif lookahead.type == TokenType.LINEFEED:
                return Discard(lookahead.line, self.get_label())
            else:
                return None
        elif lookahead.type == TokenType.TAB:
            lookahead = self.nextToken()
            if lookahead.type == TokenType.SPACE:
                return Copy(lookahead.line, self.parseNumber(), self.get_label())
            elif lookahead.type == TokenType.LINEFEED:
                return Slide(lookahead.line, self.parseNumber(), self.get_label())
            else:
                return None
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
    
    def parseLabel(self) -> int:
        lookahead = self.nextToken()
        out: int = 0

        # For the label, space is 0, tab is 1 (ends on LF; the LF is consumed)
        while lookahead.type == TokenType.SPACE or lookahead.type == TokenType.TAB:
            if lookahead.type == TokenType.SPACE:
                # Add 0 to number
                out = out << 1
            elif lookahead.type == TokenType.TAB:
                # Add 1 to number
                out = out << 1
                out += 1

            lookahead = self.nextToken()

        return out
    

    def parseFlowControl(self) -> Command | None:
        lookahead = self.nextToken()

        if lookahead.type == TokenType.LINEFEED:
            lookahead = self.nextToken()

            if lookahead.type == TokenType.LINEFEED:
                return End(lookahead.line, self.get_label())
            else:
                return None
        elif lookahead.type == TokenType.SPACE:
            lookahead = self.nextToken()
            
            if lookahead.type == TokenType.SPACE:
                # The next part of the source is a label, ending with LF
                # Will be applied to the next instruction
                self.label = self.parseLabel()
                # Recurse to parse next thing
                return self.nextCommand()
            elif lookahead.type == TokenType.LINEFEED:
                target_label = self.parseLabel()
                return Jump(lookahead.line, self.get_label(), target_label)
            elif lookahead.type == TokenType.TAB:
                return CallSub(lookahead.line, self.get_label(), self.parseLabel())
            else:
                return None
        elif lookahead.type == TokenType.TAB:
            lookahead = self.nextToken()

            if lookahead.type == TokenType.LINEFEED:
                return EndSub(lookahead.line, self.get_label())
            elif lookahead.type == TokenType.SPACE:
                return JumpZero(lookahead.line, self.get_label(), self.parseLabel())
            elif lookahead.type == TokenType.TAB:
                return JumpNegative(lookahead.line, self.get_label(), self.parseLabel())
            else:
                return None
        else:
            return None
    

    def parseIO(self) -> Command | None:
        lookahead = self.nextToken()

        if lookahead.type == TokenType.SPACE:
            lookahead = self.nextToken()

            if lookahead.type == TokenType.SPACE:
                return OutChar(lookahead.line, label=self.get_label())
            elif lookahead.type == TokenType.TAB:
                return OutNum(lookahead.line, self.get_label())
            else:
                return None
        elif lookahead.type == TokenType.TAB:
            lookahead = self.nextToken()

            if lookahead.type == TokenType.SPACE:
                return ReadChar(lookahead.line, self.get_label())
            elif lookahead.type == TokenType.TAB:
                return ReadNum(lookahead.line, self.get_label())
            else:
                return None
        else:
            return None
    

    def parseArith(self) -> Command | None:
        lookahead = self.nextToken()

        if lookahead.type == TokenType.SPACE:
            lookahead = self.nextToken()
            
            if lookahead.type == TokenType.SPACE:
                return Plus(lookahead.line, self.get_label())
            elif lookahead.type == TokenType.TAB:
                return Minus(lookahead.line, self.get_label())
            elif lookahead.type == TokenType.LINEFEED:
                return Times(lookahead.line, self.get_label())
            else:
                return None
        elif lookahead.type == TokenType.TAB:
            lookahead = self.nextToken()

            if lookahead.type == TokenType.SPACE:
                return IntDivide(lookahead.line, self.get_label())
            elif lookahead.type == TokenType.TAB:
                return Modulo(lookahead.line, self.get_label())
            else:
                return None
        else:
            return None
            
    
    def parseHeap(self) -> Command | None:
        lookahead = self.nextToken()

        if lookahead.type == TokenType.SPACE:
            return Write_Heap(lookahead.line, self.get_label())
        elif lookahead.type == TokenType.TAB:
            return Read_Heap(lookahead.line, self.get_label())
        else:
            return None
