from whitespace.Constants_errors import WORD_TYPE
from whitespace.Parser import Parser
from whitespace.Runtime import Runtime
from whitespace.Visitor import visit_flow_control

def execute(source: str, detect_readable: bool) -> None:
    p = Parser(source, detect_readable)
    program = p.allCommands()
    visit_flow_control(program)

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

def minify(source: str, detect_readable: bool) -> str:
    p = Parser(source, detect_readable)
    program = p.allCommands()
    
    out = ""

    for command in program:
        out += command.minified()
    
    return out