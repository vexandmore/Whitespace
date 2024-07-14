from whitespace.Constants_errors import WORD_TYPE
from whitespace.Parser import Parser
from whitespace.Runtime import Runtime
from whitespace.Visitor import visit_flow_control

def execute(source: str) -> None:
    p = Parser(source)
    program = p.allCommands()
    visit_flow_control(program)
    print(f"Program: {program}")

    runtime = Runtime()

    PC = 0
    while PC != -1:
        statement = program[PC]
        ret = statement.execute(runtime)
        if ret is None:
            PC += 1
        else:
            # Update PC if command is a flow control one
            PC = ret

