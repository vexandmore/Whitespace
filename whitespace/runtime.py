from whitespace.constants_errors import WORD_TYPE
from whitespace.parser import Parser
from whitespace.Heap import Heap
from array import array

def execute(source: str) -> None:
    p = Parser(source)
    program = p.allCommands()
    print(f"Program: {program}")

    stack = array(WORD_TYPE)
    heap = Heap()

    # No flow control yet
    for statement in program:
        statement.execute(stack, heap)

