from whitespace.Parser import Parser
from whitespace.Runner import minify
from whitespace.Commands import Command
import unittest

class TestMinimizer(unittest.TestCase):
    def setUp(self):
        # We don't care about line number for these tests;
        # the minifier, when applied to "readable" format files,
        # will change the line numbers
        Command.ignore_line_number = True

    def tearDown(self) -> None:
        Command.ignore_line_number = False

    def test_cat_program(self):
        original_source = """[LF][Space][Space]Mark location[Space][LF]Location space LF
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
                        [LF][LF][LF] (End)"""
        original_commands = Parser(original_source, detect_readable=True).allCommands()
        
        minimized_source = minify(original_source, detect_readable=True)
        minimized_commands = Parser(minimized_source, detect_readable=False).allCommands()

        self.assertEqual(original_commands, minimized_commands)
