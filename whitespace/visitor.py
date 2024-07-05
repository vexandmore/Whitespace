from whitespace.commands import Command, CallSub
from whitespace.constants_errors import DuplicateLabels

def visit_flow_control(prog: list[Command]):
    # Maps the label to command index (ie where the PC has to go to)
    labels: dict[int, int] = {}

    # Do first pass, finding all labels
    for (idx, command) in enumerate(prog):
        label = command.label
        if label in labels:
            raise DuplicateLabels(f"Label {label} appears both at command {command} (location {idx}) and at location {labels[label]}")
        
        labels[label] = idx
    
    for command in prog:
        if isinstance(command, CallSub):
            command.target_pc = labels[command.target_label]
