from whitespace.Heap import Heap
from abc import ABC, abstractmethod
from array import array
from typing import TextIO
from whitespace.constants_errors import WORD_TYPE
from whitespace.Heap import Heap
import sys

from whitespace.constants_errors import StackError, CannotFindJumpTarget

class Runtime():
    def __init__(self, stack: array = array(WORD_TYPE), heap: Heap = Heap(), callstack: array = array(WORD_TYPE), PC: int = 0):
        self.stack = stack
        self.heap = heap
        self.callstack = callstack
        self.PC = PC
    
    def __repr__(self) -> str:
        return f"Runtime, stack {self.stack} heap {self.heap} callstack {self.callstack} PC {self.PC}"


class Command(ABC):
    def __init__(self, line: int, label: int = -1):
        self.line = line
        self.label = label

    # Return either None, or index of where to jump to next.
    # At end of program, returns -1.
    # Can throw a StackError, HeapError, OverflowError
    @abstractmethod
    def execute(self, runtime: Runtime) -> int | None:
        pass

    def __repr__(self) -> str:
        return f"Command on line {self.line} label {self.label}"
    
    def __eq__(self, value: object) -> bool:
        if isinstance(value, Command):
            return self.line == value.line and self.label == value.label
        else:
            return False

######################
# runtime.stack Manipulation #
######################
class Push(Command):
    def __init__(self, line:int, num: int, label: int = -1):
        super().__init__(line, label)
        self.num = num
    
    def execute(self, runtime: Runtime) -> None:
        runtime.stack.append(self.num)
    
    def __eq__(self, value: object) -> bool:
        if type(value) == Push:
            return super().__eq__(value) and self.num == value.num
        else:
            return False
    
    def __repr__(self) -> str:
        return f"Push {self.num} line {self.line}"


class Duplicate(Command):
    def __init__(self, line:int, label: int = -1):
        super().__init__(line, label)
    
    def execute(self, runtime: Runtime) -> None:
        if len(runtime.stack) == 0:
            raise StackError("Empty runtime.stack")
        
        runtime.stack.append(runtime.stack[-1])
    
    def __eq__(self, value: object) -> bool:
        if type(value) == Duplicate:
            return super().__eq__(value)
        else:
            return False
    
    def __repr__(self) -> str:
        return f"Duplicate on line {self.line} label {self.label}"


class Swap(Command):
    def __init__(self, line:int, label: int = -1):
        super().__init__(line, label)
    
    def execute(self, runtime: Runtime) -> None:
        if len(runtime.stack) < 2:
            raise StackError("Need two items on the runtime.stack to swap")
        
        top, second = (runtime.stack.pop(), runtime.stack.pop())
        runtime.stack.append(top)
        runtime.stack.append(second)
    
    def __eq__(self, value: object) -> bool:
        if type(value) == Swap:
            return super().__eq__(value)
        else:
            return False
    
    def __repr__(self) -> str:
        return f"Swap on line {self.line} label {self.label}"


class Discard(Command):
    def __init__(self, line:int, label: int = -1):
        super().__init__(line, label)
    
    def execute(self, runtime: Runtime) -> None:
        if len(runtime.stack) == 0:
            raise StackError("Cannot discard on empty runtime.stack")
        runtime.stack.pop()

    def __eq__(self, value: object) -> bool:
        if type(value) == Discard:
            return super().__eq__(value)
        else:
            return False
    
    def __repr__(self) -> str:
        return f"Discard on line {self.line} label {self.label}"
    
# Copy and slide: not implemented yet

##############
# Arithmetic #
##############

class Plus(Command):
    def __init__(self, line:int, label: int = -1):
        super().__init__(line, label)
    
    def execute(self, runtime: Runtime) -> None:
        if len(runtime.stack) < 2:
            raise StackError("Need two elements to add")
        second, first = (runtime.stack.pop(), runtime.stack.pop())
        runtime.stack.append(first + second)

    def __eq__(self, value: object) -> bool:
        if type(value) == Plus:
            return super().__eq__(value)
        else:
            return False
    
    def __repr__(self) -> str:
        return f"Plus on line {self.line} label {self.label}"

class Minus(Command):
    def __init__(self, line:int, label: int = -1):
        super().__init__(line, label)
    
    def execute(self, runtime: Runtime) -> None:
        if len(runtime.stack) < 2:
            raise StackError("Need two elements to subtract")
        second, first = (runtime.stack.pop(), runtime.stack.pop())
        runtime.stack.append(first - second)

    def __eq__(self, value: object) -> bool:
        if type(value) == Minus:
            return super().__eq__(value)
        else:
            return False
    
    def __repr__(self) -> str:
        return f"Minus on line {self.line} label {self.label}"

class Times(Command):
    def __init__(self, line:int, label: int = -1):
        super().__init__(line, label)
    
    def execute(self, runtime: Runtime) -> None:
        if len(runtime.stack) < 2:
            raise StackError("Need two elements to multiply")
        second, first = (runtime.stack.pop(), runtime.stack.pop())
        runtime.stack.append(first * second)

    def __eq__(self, value: object) -> bool:
        if type(value) == Times:
            return super().__eq__(value)
        else:
            return False
    
    def __repr__(self) -> str:
        return f"Times on line {self.line} label {self.label}"


class IntDivide(Command):
    def __init__(self, line:int, label: int = -1):
        super().__init__(line, label)
    
    def execute(self, runtime: Runtime) -> None:
        if len(runtime.stack) < 2:
            raise StackError("Need two elements to int divide")
        second, first = (runtime.stack.pop(), runtime.stack.pop())
        runtime.stack.append(first // second)

    def __eq__(self, value: object) -> bool:
        if type(value) == IntDivide:
            return super().__eq__(value)
        else:
            return False
    
    def __repr__(self) -> str:
        return f"IntDivide on line {self.line} label {self.label}"


class Modulo(Command):
    def __init__(self, line:int, label: int = -1):
        super().__init__(line, label)
    
    def execute(self, runtime: Runtime) -> None:
        if len(runtime.stack) < 2:
            raise StackError("Need two elements to modulo")
        second, first = (runtime.stack.pop(), runtime.stack.pop())
        runtime.stack.append(first % second)

    def __eq__(self, value: object) -> bool:
        if type(value) == Modulo:
            return super().__eq__(value)
        else:
            return False
    
    def __repr__(self) -> str:
        return f"Modulo on line {self.line} label {self.label}"

######
# IO #
######

class OutChar(Command):
    def __init__(self, line: int, file: TextIO = sys.stdout, label: int = -1):
        self.file = file
        super().__init__(line, label)

    def execute(self, runtime: Runtime) -> None:
        if len(runtime.stack) == 0:
            raise StackError("Empty runtime.stack")

        print(chr(runtime.stack.pop()), file=self.file, end="")
    
    def __eq__(self, value: object) -> bool:
        if type(value) == OutChar:
            return super().__eq__(value)
        else:
            return False

    def __repr__(self) -> str:
        return f"Outchar on line {self.line} label {self.label}"


class OutNum(Command):
    def __init__(self, line: int, file: TextIO = sys.stdout, label: int = -1):
        self.file = file
        super().__init__(line, label)

    def execute(self, runtime: Runtime) -> None:
        if len(runtime.stack) == 0:
            raise StackError("Empty runtime.stack")

        print(runtime.stack.pop(), file=self.file, end="")
    
    def __eq__(self, value: object) -> bool:
        if type(value) == OutNum:
            return super().__eq__(value)
        else:
            return False

    def __repr__(self) -> str:
        return f"Outnum on line {self.line} label {self.label}"


class ReadChar(Command):
    def __init__(self, line: int, file: TextIO = sys.stdin, label: int = -1):
        self.file = file
        super().__init__(line, label)

    def execute(self, runtime: Runtime) -> None:
        read_byte = int(self.file.read()[0])
        runtime.stack.append(read_byte)
    
    def __eq__(self, value: object) -> bool:
        if type(value) == ReadChar:
            return super().__eq__(value)
        else:
            return False

    def __repr__(self) -> str:
        return f"Inchar on line {self.line} label {self.label}"
    

class ReadNum(Command):
    def __init__(self, line: int, file: TextIO = sys.stdin, label: int = -1):
        self.file = file
        super().__init__(line, label)

    def execute(self, runtime: Runtime) -> None:
        line = self.file.readline()
        read_int = int(line)
        runtime.stack.append(read_int)
    
    def __eq__(self, value: object) -> bool:
        if type(value) == ReadNum:
            return super().__eq__(value)
        else:
            return False

    def __repr__(self) -> str:
        return f"Inchar on line {self.line} label {self.label}"

################
# Control Flow #
################

class End(Command):
    def __init__(self, line: int, label: int = -1):
        super().__init__(line, label)

    def execute(self, runtime: Runtime) -> int | None:
        return -1

    def __eq__(self, value: object) -> bool:
        if type(value) == End:
            return super().__eq__(value)
        else:
            return False

    def __repr__(self) -> str:
        return f"End on line {self.line} label {self.label}"


class CallSub(Command):
    def __init__(self, line: int, label: int = -1, target_label: int = -1):
        self.target_label = target_label
        self.target_pc = -1 # Will be the target program counter
        super().__init__(line, label)

    def execute(self, runtime: Runtime) -> int | None:
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
        return f"Callsub on line {self.line} label {self.label}, target label {self.target_label}, PC {self.target_pc}"


class EndSub(Command):
    def __init__(self, line: int, label: int = -1):
        super().__init__(line, label)

    def execute(self, runtime: Runtime) -> int | None:
        if len(runtime.callstack) == 0:
            raise StackError("Callstack is empty, yet a end subroutine is desired")
        return runtime.callstack.pop()

    def __eq__(self, value: object) -> bool:
        if type(value) == EndSub:
            return super().__eq__(value)
        else:
            return False

    def __repr__(self) -> str:
        return f"Endsub on line {self.line} label {self.label}"


class Jump(Command):
    def __init__(self, line: int, label: int = -1, target_label: int = -1):
        super().__init__(line, label)
        self.target_label = target_label
        self.target_pc = -1 # Will be the target program counter once commands are traversed

    def execute(self, runtime: Runtime) -> int | None:
        return self.target_pc
    
    def __eq__(self, value: object) -> bool:
        if type(value) == Jump:
            return super().__eq__(value) and self.target_label == value.target_label and self.target_pc == value.target_pc
        else:
            return False

    def __repr__(self) -> str:
        return f"Jump on line {self.line} label {self.target_label}, target pc {self.target_pc}"


########
# Heap #
########

class Read_Heap(Command):
    def __init__(self, line: int, label: int = -1):
        super().__init__(line, label)

    def execute(self, runtime: Runtime) -> int | None:
        if len(runtime.stack) < 1:
            raise StackError("Need one runtime.stack elements to heap read")
        
        addr = runtime.stack.pop()
        runtime.stack.append(runtime.heap.read(addr))
        return None
    
    def __eq__(self, value: object) -> bool:
        if type(value) == Read_Heap:
            return super().__eq__(value)
        else:
            return False

    def __repr__(self) -> str:
        return f"Read heap on line {self.line} label {self.label}"

class Write_Heap(Command):
    def __init__(self, line: int, label: int = -1):
        super().__init__(line, label)

    def execute(self, runtime: Runtime) -> int | None:
        if len(runtime.stack) < 2:
            raise StackError("Need two elements to heap write")
        
        value, addr = (runtime.stack.pop(), runtime.stack.pop())
        runtime.heap.write(addr, value)
        return None
    
    def __eq__(self, value: object) -> bool:
        if type(value) == Write_Heap:
            return super().__eq__(value)
        else:
            return False

    def __repr__(self) -> str:
        return f"Write heap on line {self.line} label {self.label}"