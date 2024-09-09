from whitespace.Parser import Parser
from whitespace.Runtime import Runtime
from whitespace.Visitor import visit_flow_control
from whitespace.colours import TerminalColors

def execute(source: str, detect_readable: bool, print_out: bool, verbose: bool, debug: bool) -> None:
    p = Parser(source, detect_readable)
    program = p.allCommands()
    visit_flow_control(program)

    if print_out:
        print("Program:")
        print("\n".join(map(str, program)))
        print() # add newline

    runtime = Runtime()

    while runtime.PC != -1 and runtime.PC < len(program):
        statement = program[runtime.PC]
        if verbose or debug:
            print(TerminalColors.OKCYAN + str(statement) + TerminalColors.ENDC)
        if debug:
            while True:
                print(TerminalColors.OKBLUE + "(ws) " + TerminalColors.ENDC, end="")
                command = input()
                if command == "ni" or command == "nexti":
                    break
        runtime.PC = statement.execute(runtime)

def minify(source: str, detect_readable: bool) -> str:
    p = Parser(source, detect_readable)
    program = p.allCommands()
    
    out = ""

    for command in program:
        out += command.minified()
    
    return out