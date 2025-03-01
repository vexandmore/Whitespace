from whitespace.Commands import Command, CallSub, Jump, JumpNegative, JumpZero
from whitespace.Commands import Push, OutNum, OutChar, Discard
from whitespace.Constants_errors import DuplicateLabels

def visit_flow_control(prog: list[Command]) -> None:
    # Maps the label to command index (ie where the PC has to go to)
    labels: dict[int, int] = {}

    # Do first pass, finding all labels
    for (idx, command) in enumerate(prog):
        label = command.label
        if label != -1 and label in labels:
            raise DuplicateLabels(f"Label {label} appears both at command {command} (location {idx}) and at location {labels[label]}")
        
        labels[label] = idx
    
    for command in prog:
        if isinstance(command, CallSub):
            command.target_pc = labels[command.target_label]
        elif isinstance(command, Jump):
            command.target_pc = labels[command.target_label]
        elif isinstance(command, JumpZero):
            command.target_pc = labels[command.target_label]
        elif isinstance(command, JumpNegative):
            command.target_pc = labels[command.target_label]

def visit_asm_generation(prog: list[Command]) -> str:
    assembly = "global _start\nsection .text\n_start:\n"

    for command in prog:
        if isinstance(command, Push):
            assembly += "  push " + str(command.num) + "\n"
        elif isinstance(command, OutChar):
            assembly += "  mov rax, 1        ; write (\n"
            assembly += "  mov rdi, 1        ; STDOUT_FILENO,\n"
            assembly += "  mov rsi, rsp      ; &top_of_stack,\n"
            assembly += "  mov rdx, 1        ; 1\n"
            assembly += "  syscall           ; );\n"
        elif isinstance(command, Discard):
            assembly += "  pop rax           ; pop off the top of the stack, into rax since we don't care where it goes (and we aren't storing rax anyhow) \n"
    
    # Add exit syscall
    assembly += "; Exit with return code 0\n"
    assembly += "  mov rax, 60    ; exit(\n"
    assembly += "  mov rdi, 0     ;   EXIT_SUCCESS\n"
    assembly += "  syscall        ; );\n"


    return assembly
