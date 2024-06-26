from whitespace.Heap import Heap
from abc import ABC, abstractmethod
from array import array
from typing import TextIO
import sys

from whitespace.constants_errors import StackError


class Command(ABC):
    def __init__(self, line: int, label: int = -1):
        self.line = line
        self.label = label

    # Return either None, or index of where to jump to next.
    # At end of program, returns -1.
    # Can throw a StackError, HeapError, OverflowError
    @abstractmethod
    def execute(self, stack: array, heap: Heap) -> int | None:
        pass

    def __repr__(self) -> str:
        return f"Command on line {self.line} label {self.label}"
    
    def __eq__(self, value: object) -> bool:
        if isinstance(value, Command):
            return self.line == value.line and self.label == value.label
        else:
            return False

######################
# Stack Manipulation #
######################
class Push(Command):
    def __init__(self, line:int, num: int, label: int = -1):
        super().__init__(line, label)
        self.num = num
    
    def execute(self, stack: array, heap: Heap) -> None:
        stack.append(self.num)
    
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
    
    def execute(self, stack: array, heap: Heap) -> None:
        if len(stack) == 0:
            raise StackError("Empty stack")
        
        stack.append(stack[-1])
    
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
    
    def execute(self, stack: array, heap: Heap) -> None:
        if len(stack) < 2:
            raise StackError("Need two items on the stack to swap")
        
        top, second = (stack.pop(), stack.pop())
        stack.append(top)
        stack.append(second)
    
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
    
    def execute(self, stack: array, heap: Heap) -> None:
        if len(stack) == 0:
            raise StackError("Cannot discard on empty stack")
        stack.pop()

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
    
    def execute(self, stack: array, heap: Heap) -> None:
        if len(stack) < 2:
            raise StackError("Need two elements to add")
        second, first = (stack.pop(), stack.pop())
        stack.append(first + second)

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
    
    def execute(self, stack: array, heap: Heap) -> None:
        if len(stack) < 2:
            raise StackError("Need two elements to subtract")
        second, first = (stack.pop(), stack.pop())
        stack.append(first - second)

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
    
    def execute(self, stack: array, heap: Heap) -> None:
        if len(stack) < 2:
            raise StackError("Need two elements to multiply")
        second, first = (stack.pop(), stack.pop())
        stack.append(first * second)

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
    
    def execute(self, stack: array, heap: Heap) -> None:
        if len(stack) < 2:
            raise StackError("Need two elements to int divide")
        second, first = (stack.pop(), stack.pop())
        stack.append(first // second)

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
    
    def execute(self, stack: array, heap: Heap) -> None:
        if len(stack) < 2:
            raise StackError("Need two elements to modulo")
        second, first = (stack.pop(), stack.pop())
        stack.append(first % second)

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

    def execute(self, stack: array, heap: Heap) -> None:
        if len(stack) == 0:
            raise StackError("Empty stack")

        print(chr(stack.pop()), file=self.file, end="")
    
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

    def execute(self, stack: array, heap: Heap) -> None:
        if len(stack) == 0:
            raise StackError("Empty stack")

        print(stack.pop(), file=self.file, end="")
    
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

    def execute(self, stack: array, heap: Heap) -> None:
        read_byte = int(self.file.read()[0])
        stack.append(read_byte)
    
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

    def execute(self, stack: array, heap: Heap) -> None:
        line = self.file.readline()
        read_int = int(line)
        stack.append(read_int)
    
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

    def execute(self, stack: array, heap: Heap) -> int | None:
        return -1

    def __eq__(self, value: object) -> bool:
        if type(value) == End:
            return super().__eq__(value)
        else:
            return False

    def __repr__(self) -> str:
        return f"End on line {self.line} label {self.label}"

########
# Heap #
########

class Read_Heap(Command):
    def __init__(self, line: int, label: int = -1):
        super().__init__(line, label)

    def execute(self, stack: array, heap: Heap) -> int | None:
        if len(stack) < 1:
            raise StackError("Need one stack elements to heap read")
        
        addr = stack.pop()
        stack.append(heap.read(addr))
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

    def execute(self, stack: array, heap: Heap) -> int | None:
        if len(stack) < 2:
            raise StackError("Need two elements to heap write")
        
        value, addr = (stack.pop(), stack.pop())
        heap.write(addr, value)
        return None
    
    def __eq__(self, value: object) -> bool:
        if type(value) == Write_Heap:
            return super().__eq__(value)
        else:
            return False

    def __repr__(self) -> str:
        return f"Write heap on line {self.line} label {self.label}"