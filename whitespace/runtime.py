from whitespace.constants_errors import WORD_TYPE
from whitespace.parser import Parser
from whitespace.commands import Runtime
from whitespace.visitor import visit_flow_control

def execute(source: str) -> None:
    p = Parser(source)
    program = p.allCommands()
    visit_flow_control(program)
    print(f"Program: {program}")

    runtime = Runtime()

    # No flow control yet
    PC = 0
    while PC != -1:
        statement = program[PC]
        ret = statement.execute(runtime)
        if ret is not None:
            # Update PC if command is a flow control one
            PC = ret

