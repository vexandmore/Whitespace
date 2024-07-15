from whitespace.Commands import Command, CallSub, Jump, JumpNegative, JumpZero
from whitespace.Constants_errors import DuplicateLabels
from whitespace.Parser import Parser
from whitespace.Visitor import visit_flow_control
from whitespace.Constants_errors import DuplicateLabels

import unittest

class TestVisitor(unittest.TestCase):
    def test_duplicates_detected(self):
        p = Parser("[LF][Space][Space] [Tab][Space] [LF] Mark with label 2" + 
                   "[Space][Space] [Space][Space][LF] add 0 to stack" + 
                   "[LF][Space][Space] [Tab][Space] [LF] Mark with label 2" + 
                   "[Space][Space] [Space][Tab][LF] add 1 to stack", detect_readable=True)
        program = p.allCommands()
        self.assertRaises(DuplicateLabels, lambda: visit_flow_control(program))
    
