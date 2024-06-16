from enum import Enum
from abc import ABC, abstractmethod
from array import array


class Command(ABC):
    def __init__(self, line: int):
        self.line = line

    @abstractmethod
    def execute(self, stack: array, heap: dict[int, int]) -> None:
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
    def __init__(self, line: int):
        super().__init__(line)

    def execute(self, stack: array, heap: dict[int, int]) -> None:
        print(stack.pop(), end="")
    
    def __eq__(self, value: object) -> bool:
        if type(value) == OutChar:
            return super().__eq__(value)
        else:
            return False

    def __repr__(self) -> str:
        return f"Outchar on line {self.line}"


class End(Command):
    def __init__(self, line: int):
        super().__init__(line)

    def execute(self, stack: array, heap: dict[int, int]) -> None:
        quit() 

    def __repr__(self) -> str:
        return f"End on line {self.line}"
