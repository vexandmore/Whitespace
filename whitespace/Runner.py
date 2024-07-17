from whitespace.Constants_errors import WORD_TYPE
from whitespace.Parser import Parser
from whitespace.Runtime import Runtime
from whitespace.Visitor import visit_flow_control

def execute(source: str, detect_readable: bool) -> None:
    p = Parser(source, detect_readable)
    program = p.allCommands()
    visit_flow_control(program)

    runtime = Runtime()

    while runtime.PC != -1 and runtime.PC < len(program):
        statement = program[runtime.PC]
        runtime.PC = statement.execute(runtime)

def minify(source: str, detect_readable: bool) -> str:
    p = Parser(source, detect_readable)
    program = p.allCommands()
    
    out = ""

    for command in program:
        out += command.minified()
    
    return out