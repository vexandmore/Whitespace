from whitespace.commands import Push, End, OutChar, OutNum, ReadChar, Plus
from whitespace.commands import ReadNum, Duplicate, StackError, Swap, Discard
import unittest
import io
from array import array

class TestParser(unittest.TestCase):

    ######
    # IO #
    ######
    def test_read_num(self):
        # Setup
        file = io.BytesIO(b"  \t 103\n")
        read_num = ReadNum(1, file)
        stack = array('b')
        stack.append(98)

        # Run
        ret = read_num.execute(stack, {})

        # Assert
        self.assertEqual(ret, None)
        self.assertEqual(len(stack), 2)
        self.assertEqual(stack[0], 98)
        self.assertEqual(stack[1], 103)
    

    def test_read_char(self):
        # Setup
        file = io.BytesIO(b"a")
        read_num = ReadChar(1, file)
        stack = array('b')
        stack.append(98)

        # Run
        ret = read_num.execute(stack, {})

        # Assert
        self.assertEqual(ret, None)
        self.assertEqual(len(stack), 2)
        self.assertEqual(stack[0], 98)
        self.assertEqual(stack[1], 97)
    
    def test_out_num(self):
        # Setup
        file = io.StringIO("")
        out_char = OutNum(1, file)
        stack = array('b')
        stack.append(97)

        # Run
        ret = out_char.execute(stack, {})

        # Assert
        self.assertEqual(ret, None)
        self.assertEqual(file.getvalue(), "97")
        self.assertEqual(len(stack), 0)


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
    
    ######################
    # Stack Manipulation #
    ######################
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

    def test_duplicate_throws(self):
        # Setup
        file = io.StringIO("")
        duplicate = Duplicate(1)
        stack = array('b')
        
        # Run and Assert
        self.assertRaises(StackError, lambda: duplicate.execute(stack, {}))

    def test_duplicate(self):
        # Setup
        file = io.StringIO("")
        duplicate = Duplicate(1)
        stack = array('b')
        stack.append(24)
        stack.append(78)
        
        # Run
        ret = duplicate.execute(stack, {})

        # Assert
        self.assertEqual(ret, None)
        self.assertEqual(file.getvalue(), "")
        self.assertEqual(len(stack), 3)
        self.assertEqual(stack[0], 24)
        self.assertEqual(stack[1], 78)
        self.assertEqual(stack[2], 78)
    

    def test_swap(self):
        # Setup
        file = io.StringIO("")
        swap = Swap(1)
        stack = array('b')
        stack.append(24)
        stack.append(78)
        stack.append(44)
        
        # Run
        ret = swap.execute(stack, {})

        # Assert
        self.assertEqual(ret, None)
        self.assertEqual(file.getvalue(), "")
        self.assertEqual(len(stack), 3)
        self.assertEqual(stack[0], 24)
        self.assertEqual(stack[1], 44)
        self.assertEqual(stack[2], 78)
    
    def test_swap_throws(self):
        # Setup
        file = io.StringIO("")
        swap = Swap(1)
        stack = array('b')
        
        # Run and Assert
        self.assertRaises(StackError, lambda: swap.execute(stack, {}))


    def test_discard(self):
        # Setup
        file = io.StringIO("")
        discard = Discard(1)
        stack = array('b')
        stack.append(24)
        stack.append(78)
        
        # Run
        ret = discard.execute(stack, {})

        # Assert
        self.assertEqual(ret, None)
        self.assertEqual(file.getvalue(), "")
        self.assertEqual(len(stack), 1)
        self.assertEqual(stack[0], 24)
    
    def test_discard_throws(self):
        # Setup
        file = io.StringIO("")
        discard = Discard(1)
        stack = array('b')
        
        # Run and Assert
        self.assertRaises(StackError, lambda: discard.execute(stack, {}))

    def test_plus(self):
        # Setup
        file = io.StringIO("")
        plus = Plus(1)
        stack = array('b')
        stack.append(24)
        stack.append(78)
        
        # Run
        ret = plus.execute(stack, {})

        # Assert
        self.assertEqual(ret, None)
        self.assertEqual(file.getvalue(), "")
        self.assertEqual(len(stack), 1)
        self.assertEqual(stack[0], 24 + 78)

    def test_plus_throws(self):
        # Setup
        file = io.StringIO("")
        plus = Plus(1)
        stack = array('b')
        stack.append(34) # need two for plus
        
        # Run and Assert
        self.assertRaises(StackError, lambda: plus.execute(stack, {}))

    ################
    # Control Flow #
    ################
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
