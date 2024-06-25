from whitespace.parser import Parser
from array import array

def execute(source: str) -> None:
    p = Parser(source)
    program = p.allCommands()
    print(f"Program: {program}")

    stack = array('b')
    heap: dict[int, int] = {}

    # No flow control yet
    for statement in program:
        statement.execute(stack, heap)

