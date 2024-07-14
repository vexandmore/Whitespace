from whitespace.Constants_errors import WORD_TYPE
from whitespace.Heap import Heap


from array import array


class Runtime():
    def __init__(self, stack: array | None = None, heap: Heap | None = None, callstack: array | None = None, PC: int = 0):
        self.stack = stack if stack is not None else array(WORD_TYPE)
        self.heap = heap if heap is not None else Heap()
        self.callstack = callstack if callstack is not None else array(WORD_TYPE)
        self.PC = PC

    def __repr__(self) -> str:
        return f"Runtime, stack {self.stack} heap {self.heap} callstack {self.callstack} PC {self.PC}"