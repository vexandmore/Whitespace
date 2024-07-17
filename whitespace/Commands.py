from whitespace.Constants_errors import StackError, CannotFindJumpTarget
from whitespace.Runtime import Runtime

from abc import ABC, abstractmethod

class Command(ABC):
    # Set to True to ignore line number in equality comparisons
    ignore_line_number = False

    def __init__(self, line: int, label: int = -1):
        self.line = line
        self.label = label

    # Return either None, or index of where to jump to next.
    # At end of program, returns -1.
    # Can throw a StackError, HeapError, OverflowError
    @abstractmethod
    def execute(self, runtime: Runtime) -> int:
        pass

    # Used to print out label only if it exists (ie is not -1)
    def label_repr(self) -> str:
        return f"label {self.label}" if self.label != -1 else ""

    def __repr__(self) -> str:
        return f"Command on line {self.line} " + self.label_repr()
    
    def __eq__(self, value: object) -> bool:
        if isinstance(value, Command):
            return (self.line == value.line or Command.ignore_line_number) and self.label == value.label
        else:
            return False
    
    # Returns the minimum syntax for this command
    # On the Command class, returns the "set label" if there is a label
    @abstractmethod
    def minified(self) -> str:
        if self.label != -1:
            return "\n  " + self.encodeLabel(self.label)
        else:
            return ""

    
    # Encode a number into its whitespace representation
    def encodeNumber(self, n: int) -> str:
        if n == 0:
            return "  \n"

        out = ""
        signchar = " " if n > 0 else "\t"
        while n > 0 or n < 0:
            bit = n % 2
            out += " " if bit == 0 else "\t"
            n = n // 2
        out = out[::-1] # reverse string
        return signchar + out + "\n"
    

    # Encode a label into its whitespace representation
    def encodeLabel(self, n: int) -> str:
        if n == 0:
            return " \n"
        
        out = ""
        while n > 0:
            bit = n % 2
            out += " " if bit == 0 else "\t"
            n = n // 2
        out = out[::-1] # reverse string
        out += "\n"
        return out
        

######################
# Stack Manipulation #
######################
class Push(Command):
    def __init__(self, line:int, num: int, label: int = -1):
        super().__init__(line, label)
        self.num = num
    
    def execute(self, runtime: Runtime) -> int:
        runtime.stack.append(self.num)
        return runtime.PC + 1
    
    def __eq__(self, value: object) -> bool:
        if type(value) == Push:
            return super().__eq__(value) and self.num == value.num
        else:
            return False
    
    def __repr__(self) -> str:
        return f"Push {self.num} line {self.line} " + self.label_repr()
    
    def minified(self) -> str:
        return super().minified() + "  " + self.encodeNumber(self.num)


class Duplicate(Command):
    def __init__(self, line:int, label: int = -1):
        super().__init__(line, label)
    
    def execute(self, runtime: Runtime) -> int:
        if len(runtime.stack) == 0:
            raise StackError("Empty runtime.stack")
        
        runtime.stack.append(runtime.stack[-1])
        return runtime.PC + 1
    
    def __eq__(self, value: object) -> bool:
        if type(value) == Duplicate:
            return super().__eq__(value)
        else:
            return False
    
    def __repr__(self) -> str:
        return f"Duplicate on line {self.line} " + self.label_repr()
    
    def minified(self) -> str:
        return super().minified() + " \n "


class Swap(Command):
    def __init__(self, line:int, label: int = -1):
        super().__init__(line, label)
    
    def execute(self, runtime: Runtime) -> int:
        if len(runtime.stack) < 2:
            raise StackError("Need two items on the runtime.stack to swap")
        
        top, second = (runtime.stack.pop(), runtime.stack.pop())
        runtime.stack.append(top)
        runtime.stack.append(second)

        return runtime.PC + 1
    
    def __eq__(self, value: object) -> bool:
        if type(value) == Swap:
            return super().__eq__(value)
        else:
            return False
    
    def __repr__(self) -> str:
        return f"Swap on line {self.line} " + self.label_repr()
    
    def minified(self) -> str:
        return super().minified() + " \n\t"

class Discard(Command):
    def __init__(self, line:int, label: int = -1):
        super().__init__(line, label)
    
    def execute(self, runtime: Runtime) -> int:
        if len(runtime.stack) == 0:
            raise StackError("Cannot discard on empty runtime.stack")
        runtime.stack.pop()

        return runtime.PC + 1

    def __eq__(self, value: object) -> bool:
        if type(value) == Discard:
            return super().__eq__(value)
        else:
            return False
    
    def __repr__(self) -> str:
        return f"Discard on line {self.line} " + self.label_repr()
    
    def minified(self) -> str:
        return super().minified() + " \n\n"
    
# Copy and slide: not implemented yet

##############
# Arithmetic #
##############

class Plus(Command):
    def __init__(self, line:int, label: int = -1):
        super().__init__(line, label)
    
    def execute(self, runtime: Runtime) -> int:
        if len(runtime.stack) < 2:
            raise StackError("Need two elements to add")
        second, first = (runtime.stack.pop(), runtime.stack.pop())
        runtime.stack.append(first + second)

        return runtime.PC + 1

    def __eq__(self, value: object) -> bool:
        if type(value) == Plus:
            return super().__eq__(value)
        else:
            return False
    
    def __repr__(self) -> str:
        return f"Plus on line {self.line} " + self.label_repr()
    
    def minified(self) -> str:
        return super().minified() + "\t   "

class Minus(Command):
    def __init__(self, line:int, label: int = -1):
        super().__init__(line, label)
    
    def execute(self, runtime: Runtime) -> int:
        if len(runtime.stack) < 2:
            raise StackError("Need two elements to subtract")
        second, first = (runtime.stack.pop(), runtime.stack.pop())
        runtime.stack.append(first - second)

        return runtime.PC + 1

    def __eq__(self, value: object) -> bool:
        if type(value) == Minus:
            return super().__eq__(value)
        else:
            return False
    
    def __repr__(self) -> str:
        return f"Minus on line {self.line} " + self.label_repr()
    
    def minified(self) -> str:
        return super().minified() + "\t  \t"

class Times(Command):
    def __init__(self, line:int, label: int = -1):
        super().__init__(line, label)
    
    def execute(self, runtime: Runtime) -> int:
        if len(runtime.stack) < 2:
            raise StackError("Need two elements to multiply")
        second, first = (runtime.stack.pop(), runtime.stack.pop())
        runtime.stack.append(first * second)

        return runtime.PC + 1

    def __eq__(self, value: object) -> bool:
        if type(value) == Times:
            return super().__eq__(value)
        else:
            return False
    
    def __repr__(self) -> str:
        return f"Times on line {self.line} " + self.label_repr()
    
    def minified(self) -> str:
        return super().minified() + "\t  \n"


class IntDivide(Command):
    def __init__(self, line:int, label: int = -1):
        super().__init__(line, label)
    
    def execute(self, runtime: Runtime) -> int:
        if len(runtime.stack) < 2:
            raise StackError("Need two elements to int divide")
        second, first = (runtime.stack.pop(), runtime.stack.pop())
        runtime.stack.append(first // second)

        return runtime.PC + 1

    def __eq__(self, value: object) -> bool:
        if type(value) == IntDivide:
            return super().__eq__(value)
        else:
            return False
    
    def __repr__(self) -> str:
        return f"IntDivide on line {self.line} " + self.label_repr()
    
    def minified(self) -> str:
        return super().minified() + "\t \t "


class Modulo(Command):
    def __init__(self, line:int, label: int = -1):
        super().__init__(line, label)
    
    def execute(self, runtime: Runtime) -> int:
        if len(runtime.stack) < 2:
            raise StackError("Need two elements to modulo")
        second, first = (runtime.stack.pop(), runtime.stack.pop())
        runtime.stack.append(first % second)

        return runtime.PC + 1

    def __eq__(self, value: object) -> bool:
        if type(value) == Modulo:
            return super().__eq__(value)
        else:
            return False
    
    def __repr__(self) -> str:
        return f"Modulo on line {self.line} " + self.label_repr()
    
    def minified(self) -> str:
        return super().minified() + "\t \t\t"

######
# IO #
######

class OutChar(Command):
    def __init__(self, line: int, label: int = -1):
        super().__init__(line, label)

    def execute(self, runtime: Runtime) -> int:
        if len(runtime.stack) == 0:
            raise StackError("Empty runtime.stack")

        print(chr(runtime.stack.pop()), file=runtime.file_out, end="")

        return runtime.PC + 1
    
    def __eq__(self, value: object) -> bool:
        if type(value) == OutChar:
            return super().__eq__(value)
        else:
            return False

    def __repr__(self) -> str:
        return f"Outchar on line {self.line} " + self.label_repr()
    
    def minified(self) -> str:
        return super().minified() + "\t\n  "


class OutNum(Command):
    def __init__(self, line: int, label: int = -1):
        super().__init__(line, label)

    def execute(self, runtime: Runtime) -> int:
        if len(runtime.stack) == 0:
            raise StackError("Empty runtime.stack")

        print(runtime.stack.pop(), file=runtime.file_out, end="")

        return runtime.PC + 1
    
    def __eq__(self, value: object) -> bool:
        if type(value) == OutNum:
            return super().__eq__(value)
        else:
            return False

    def __repr__(self) -> str:
        return f"Outnum on line {self.line} " + self.label_repr()
    
    def minified(self) -> str:
        return super().minified() + "\t\n \t"


class ReadChar(Command):
    def __init__(self, line: int, label: int = -1):
        super().__init__(line, label)

    def execute(self, runtime: Runtime) -> int:
        read_byte = int(runtime.file_in.read()[0])
        runtime.stack.append(read_byte)

        return runtime.PC + 1
    
    def __eq__(self, value: object) -> bool:
        if type(value) == ReadChar:
            return super().__eq__(value)
        else:
            return False

    def __repr__(self) -> str:
        return f"Inchar on line {self.line} " + self.label_repr()
    
    def minified(self) -> str:
        return super().minified() + "\t\n\t "
    

class ReadNum(Command):
    def __init__(self, line: int, label: int = -1):
        super().__init__(line, label)

    def execute(self, runtime: Runtime) -> int:
        line = runtime.file_in.readline()
        read_int = int(line)
        runtime.stack.append(read_int)

        return runtime.PC + 1
    
    def __eq__(self, value: object) -> bool:
        if type(value) == ReadNum:
            return super().__eq__(value)
        else:
            return False

    def __repr__(self) -> str:
        return f"Inchar on line {self.line} " + self.label_repr()
    
    def minified(self) -> str:
        return super().minified() + "\t\n\t\t"

################
# Control Flow #
################

class End(Command):
    def __init__(self, line: int, label: int = -1):
        super().__init__(line, label)

    def execute(self, runtime: Runtime) -> int:
        return -1

    def __eq__(self, value: object) -> bool:
        if type(value) == End:
            return super().__eq__(value)
        else:
            return False

    def __repr__(self) -> str:
        return f"End on line {self.line} " + self.label_repr()
    
    def minified(self) -> str:
        return super().minified() + "\n\n\n"


class CallSub(Command):
    def __init__(self, line: int, label: int = -1, target_label: int = -1):
        self.target_label = target_label
        self.target_pc = -1 # Will be the target program counter
        super().__init__(line, label)

    def execute(self, runtime: Runtime) -> int:
        if self.target_pc != -1:
            runtime.callstack.append(runtime.PC)
            return self.target_pc
        else:
            raise CannotFindJumpTarget("This node was not visited, doesn't have the target PC")

    def __eq__(self, value: object) -> bool:
        if type(value) == CallSub:
            return super().__eq__(value) and self.target_label == value.target_label and self.target_pc == value.target_pc
        else:
            return False

    def __repr__(self) -> str:
        return f"Callsub on line {self.line} target label {self.target_label}, PC {self.target_pc} " + self.label_repr()
    
    def minified(self) -> str:
        return super().minified() + "\n \t" + self.encodeLabel(self.target_label)


class EndSub(Command):
    def __init__(self, line: int, label: int = -1):
        super().__init__(line, label)

    def execute(self, runtime: Runtime) -> int:
        if len(runtime.callstack) == 0:
            raise StackError("Callstack is empty, yet a end subroutine is desired")
        return runtime.callstack.pop()

    def __eq__(self, value: object) -> bool:
        if type(value) == EndSub:
            return super().__eq__(value)
        else:
            return False

    def __repr__(self) -> str:
        return f"Endsub on line {self.line} " + self.label_repr()
    
    def minified(self) -> str:
        return super().minified() + "\n\t\n"


class Jump(Command):
    def __init__(self, line: int, label: int = -1, target_label: int = -1):
        super().__init__(line, label)
        self.target_label = target_label
        self.target_pc = -1 # Will be the target program counter once commands are traversed

    def execute(self, runtime: Runtime) -> int:
        return self.target_pc
    
    def __eq__(self, value: object) -> bool:
        if type(value) == Jump:
            return super().__eq__(value) and self.target_label == value.target_label and self.target_pc == value.target_pc
        else:
            return False

    def __repr__(self) -> str:
        return f"Jump on line {self.line} to label {self.target_label}, target pc {self.target_pc}"
    
    def minified(self) -> str:
        return super().minified() + "\n \n" + self.encodeLabel(self.target_label)


class JumpZero(Command):
    def __init__(self, line: int, label: int = -1, target_label: int = -1):
        super().__init__(line, label)
        self.target_label = target_label
        self.target_pc = -1 # Will be the target program counter once commands are traversed

    def execute(self, runtime: Runtime) -> int:
        if len(runtime.stack) == 0:
            raise StackError("Stack is empty, yet a jump if top of stack is 0 is desired")
        jump = runtime.stack[-1] == 0
        return self.target_pc if jump else runtime.PC + 1
    
    def __eq__(self, value: object) -> bool:
        if type(value) == JumpZero:
            return super().__eq__(value) and self.target_label == value.target_label and self.target_pc == value.target_pc
        else:
            return False

    def __repr__(self) -> str:
        return f"Jump if zero on line {self.line} to label {self.target_label}, target pc {self.target_pc}"
    
    def minified(self) -> str:
        return super().minified() + "\n\t " + self.encodeLabel(self.target_label)


class JumpNegative(Command):
    def __init__(self, line: int, label: int = -1, target_label: int = -1):
        super().__init__(line, label)
        self.target_label = target_label
        self.target_pc = -1 # Will be the target program counter once commands are traversed

    def execute(self, runtime: Runtime) -> int:
        if len(runtime.stack) == 0:
            raise StackError("Stack is empty, yet a jump if top of stack is negative is desired")
        jump = runtime.stack[-1] < 0
        return self.target_pc if jump else runtime.PC + 1
    
    def __eq__(self, value: object) -> bool:
        if type(value) == JumpNegative:
            return super().__eq__(value) and self.target_label == value.target_label and self.target_pc == value.target_pc
        else:
            return False

    def __repr__(self) -> str:
        return f"Jump if zero on line {self.line} to label {self.target_label}, target pc {self.target_pc}"
    
    def minified(self) -> str:
        return super().minified() + "\n\t\t" + self.encodeLabel(self.target_label)


########
# Heap #
########

class Read_Heap(Command):
    def __init__(self, line: int, label: int = -1):
        super().__init__(line, label)

    def execute(self, runtime: Runtime) -> int:
        if len(runtime.stack) < 1:
            raise StackError("Need one runtime.stack elements to heap read")

        addr = runtime.stack.pop()
        runtime.stack.append(runtime.heap.read(addr))
        return runtime.PC + 1
    
    def __eq__(self, value: object) -> bool:
        if type(value) == Read_Heap:
            return super().__eq__(value)
        else:
            return False

    def __repr__(self) -> str:
        return f"Read heap on line {self.line} " + self.label_repr()
    
    def minified(self) -> str:
        return super().minified() + "\t\t\t"

class Write_Heap(Command):
    def __init__(self, line: int, label: int = -1):
        super().__init__(line, label)

    def execute(self, runtime: Runtime) -> int:
        if len(runtime.stack) < 2:
            raise StackError("Need two elements to heap write")
        
        value, addr = (runtime.stack.pop(), runtime.stack.pop())
        runtime.heap.write(addr, value)
        return runtime.PC + 1
    
    def __eq__(self, value: object) -> bool:
        if type(value) == Write_Heap:
            return super().__eq__(value)
        else:
            return False

    def __repr__(self) -> str:
        return f"Write heap on line {self.line} " + self.label_repr()
    
    def minified(self) -> str:
        return super().minified() + "\t\t "