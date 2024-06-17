from whitespace.tokenizer import Tokenizer, Token, TokenType
from whitespace.parser import Command, Push, End, OutChar, Parser
import unittest
import io
from array import array

class TestParser(unittest.TestCase):
    def test_out_char(self):
        # Setup
        file = io.StringIO("")
        out_char = OutChar(1, file)
        stack = array('b')
        stack.append(97)

        # Run
        ret = out_char.execute(stack, {})

        # Assert
        self.assertEqual(ret, None)
        self.assertEqual(file.getvalue(), "a")
        self.assertEqual(len(stack), 0)
    
    def test_push(self):
        # Setup
        file = io.StringIO("")
        push = Push(1, 32)
        stack = array('b')
        
        # Run
        ret = push.execute(stack, {})

        # Assert
        self.assertEqual(ret, None)
        self.assertEqual(file.getvalue(), "")
        self.assertEqual(len(stack), 1)
        self.assertEqual(stack[0], 32)
    
    def test_end(self):
        # Setup
        file = io.StringIO("")
        end = End(1)
        stack = array('b')
        
        # Run
        ret = end.execute(stack, {})

        # Assert
        self.assertEqual(ret, -1)
        self.assertEqual(file.getvalue(), "")
        self.assertEqual(len(stack), 0)

if __name__ == "__main__":
    unittest.main()
