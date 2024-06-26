[LF][Space][Space]Mark location[Space][LF]Location space LF
[Space][Space]Push number to stack[Space]+[Tab]1[LF] (push 1 on stack)
[Tab][LF][Tab][Space] Read char and place it on top of stack
[Space][Space]Push number[Space]+[Tab]1[LF] (push 1 on stack) 
[Tab][Tab]Heap [Tab] retrieve (pop top of stack and heap retrieve; in this case, heap retrieve from 1)
[Tab][LF][Space][Space] Output char at top of stack
[Space][Space]Push num to stack[Space]+[Tab]1[LF] (push 1 to stack)
[Tab][Tab][Tab] (retrieve heap at address on stack; retrieve from heap at 1)
[LF][Tab][Space] (Jump if zero)[Tab][LF] (Jump to Tab if zero at stack)
[LF][Space][LF] (jump) [Space][LF] Jump to label Space LF
[LF][Space][Space](Mark location) [Tab][LF] (Mark Tab LF)
[LF][LF][LF] (End)