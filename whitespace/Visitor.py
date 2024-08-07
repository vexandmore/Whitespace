from whitespace.Commands import Command, CallSub, Jump, JumpNegative, JumpZero
from whitespace.Constants_errors import DuplicateLabels

def visit_flow_control(prog: list[Command]):
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
