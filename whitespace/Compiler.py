from whitespace.Parser import Parser
from whitespace.Runtime import Runtime
from whitespace.Visitor import visit_flow_control, visit_asm_generation
import subprocess

def generate_asm(source: str, detect_readable: bool, print_out: bool, verbose: bool) -> str:
    p = Parser(source, detect_readable)
    program = p.allCommands()
    visit_flow_control(program)

    if print_out:
        print("Program:")
        print("\n".join(map(str, program)))
        print() # add newline
    
    return visit_asm_generation(program)

# NOTE: assumes executable_name does not end with an extension
def compile(file_contents: str, executable_name: str, detect_readable: bool, print_out: bool, verbose: bool) -> None:
    assembly_filename = executable_name + ".s"
    object_filename = executable_name + ".o"

    assembly = generate_asm(file_contents, detect_readable, print_out, verbose)
    with open(assembly_filename, "w", encoding="utf-8") as f:
        # Write assembly so it can be compiled and linked
        f.write(assembly)
    
    # Now, compile to object file with nasm and link with ld
    subprocess.run(["nasm", "-f", "elf64", "-o", object_filename, assembly_filename])
    subprocess.run(["ld", "-o", executable_name, object_filename])
   
