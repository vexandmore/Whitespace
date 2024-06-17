from enum import Enum
from abc import ABC, abstractmethod
from array import array
from typing import TextIO
import sys

class Command(ABC):
    def __init__(self, line: int):
        self.line = line

    # Return either None, or index of where to jump to next.
    # At end of program, returns -1.
    # Can throw a StackError or a HeapError
    @abstractmethod
    def execute(self, stack: array, heap: dict[int, int]) -> int | None:
        pass

    def __repr__(self) -> str:
        return f"Command on line {self.line}"
    
    def __eq__(self, value: object) -> bool:
        if isinstance(value, Command):
            return self.line == value.line
        else:
            return False


class Push(Command):
    def __init__(self, line:int, num: int):
        super().__init__(line)
        self.num = num
    
    def execute(self, stack: array, heap: dict[int, int]) -> None:
        stack.append(self.num)
    
    def __eq__(self, value: object) -> bool:
        if type(value) == Push:
            return super().__eq__(value) and self.num == value.num
        else:
            return False
    
    def __repr__(self) -> str:
        return f"Push {self.num} line {self.line}"


class OutChar(Command):
    def __init__(self, line: int, file: TextIO = sys.stdout):
        self.file = file
        super().__init__(line)

    def execute(self, stack: array, heap: dict[int, int]) -> None:
        print(chr(stack.pop()), file=self.file, end="")
    
    def __eq__(self, value: object) -> bool:
        if type(value) == OutChar:
            return super().__eq__(value)
        else:
            return False

    def __repr__(self) -> str:
        return f"Outchar on line {self.line}"


class OutNum(Command):
    def __init__(self, line: int, file: TextIO = sys.stdout):
        self.file = file
        super().__init__(line)

    def execute(self, stack: array, heap: dict[int, int]) -> None:
        print(stack.pop(), file=self.file, end="")
    
    def __eq__(self, value: object) -> bool:
        if type(value) == OutChar:
            return super().__eq__(value)
        else:
            return False

    def __repr__(self) -> str:
        return f"Outnum on line {self.line}"


# class ReadChar(Command):
#     def __init__(self, line: int, file: TextIO = sys.stdin):
#         self.file = file
#         super().__init__(line)

#     def execute(self, stack: array, heap: dict[int, int]) -> None:
#         stack.append(self.file.read())
    
#     def __eq__(self, value: object) -> bool:
#         if type(value) == OutChar:
#             return super().__eq__(value)
#         else:
#             return False

#     def __repr__(self) -> str:
#         return f"Inchar on line {self.line}"


class End(Command):
    def __init__(self, line: int):
        super().__init__(line)

    def execute(self, stack: array, heap: dict[int, int]) -> int | None:
        return -1

    def __repr__(self) -> str:
        return f"End on line {self.line}"
