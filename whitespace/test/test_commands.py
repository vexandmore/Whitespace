from whitespace.Commands import Push, End, OutChar, OutNum, ReadChar, Plus, Minus, Times, IntDivide, Modulo
from whitespace.Commands import ReadNum, Duplicate, Swap, Discard, Read_Heap, Write_Heap
from whitespace.Commands import CallSub, EndSub, Jump, JumpZero, JumpNegative
from whitespace.Commands import Copy, Slide
from whitespace.Constants_errors import WORD_TYPE, StackError
from whitespace.Heap import Heap
from whitespace.Runtime import Runtime

import unittest
import io
from array import array


class TestCommands(unittest.TestCase):

    ######
    # IO #
    ######
    def test_read_num(self):
        # Setup
        file = io.StringIO("  \t 103\n")
        read_num = ReadNum(1)
        stack = array(WORD_TYPE)
        stack.append(98)

        # Run
        runtime = Runtime(stack=stack, file_in=file)
        ret = read_num.execute(runtime)

        # Assert
        self.assertEqual(ret, 1)
        self.assertEqual(len(stack), 0)
        self.assertEqual(runtime.heap.read(98), 103)
    
    def test_read_num_throws(self):
        # Setup
        file = io.StringIO("  \t 103\n")
        read_num = ReadNum(1)
        stack = array(WORD_TYPE)

        # Run/assert
        runtime = Runtime(stack=stack, file_in=file)
        self.assertRaises(StackError, lambda: read_num.execute(runtime))
    

    def test_read_char(self):
        # Setup
        file = io.StringIO("a")
        read_num = ReadChar(1)
        stack = array(WORD_TYPE)
        stack.append(98)

        # Run
        runtime = Runtime(stack=stack, file_in=file)
        ret = read_num.execute(runtime)

        # Assert
        self.assertEqual(ret, 1)
        self.assertEqual(len(stack), 0)
        self.assertEqual(runtime.heap.read(98), 97)
    
    def test_read_char_throws(self):
        # Setup
        file = io.StringIO("  \t 103\n")
        read_char = ReadChar(1)
        stack = array(WORD_TYPE)

        # Run/assert
        runtime = Runtime(stack=stack, file_in=file)
        self.assertRaises(StackError, lambda: read_char.execute(runtime))
    
    def test_out_num(self):
        # Setup
        file = io.StringIO("")
        out_char = OutNum(1)
        stack = array(WORD_TYPE)
        stack.append(97)

        # Run
        ret = out_char.execute(Runtime(stack=stack, file_out=file))

        # Assert
        self.assertEqual(ret, 1)
        self.assertEqual(file.getvalue(), "97")
        self.assertEqual(len(stack), 0)


    def test_out_char(self):
        # Setup
        file = io.StringIO("")
        out_char = OutChar(1)
        stack = array(WORD_TYPE)
        stack.append(97)

        # Run
        ret = out_char.execute(Runtime(stack=stack, file_out=file))

        # Assert
        self.assertEqual(ret, 1)
        self.assertEqual(file.getvalue(), "a")
        self.assertEqual(len(stack), 0)
    
    ######################
    # Stack Manipulation #
    ######################
    def test_push(self):
        # Setup
        push = Push(1, 32)
        stack = array(WORD_TYPE)
        
        # Run
        ret = push.execute(Runtime(stack))

        # Assert
        self.assertEqual(ret, 1)
        self.assertEqual(len(stack), 1)
        self.assertEqual(stack[0], 32)

    def test_duplicate_throws(self):
        # Setup
        duplicate = Duplicate(1)
        stack = array(WORD_TYPE)
        
        # Run and Assert
        self.assertRaises(StackError, lambda: duplicate.execute(Runtime(stack)))

    def test_duplicate(self):
        # Setup
        duplicate = Duplicate(1)
        stack = array(WORD_TYPE)
        stack.append(24)
        stack.append(78)
        
        # Run
        ret = duplicate.execute(Runtime(stack))

        # Assert
        self.assertEqual(ret, 1)
        self.assertEqual(len(stack), 3)
        self.assertEqual(stack[0], 24)
        self.assertEqual(stack[1], 78)
        self.assertEqual(stack[2], 78)
    

    def test_swap(self):
        # Setup
        swap = Swap(1)
        stack = array(WORD_TYPE)
        stack.append(24)
        stack.append(78)
        stack.append(44)
        
        # Run
        ret = swap.execute(Runtime(stack))

        # Assert
        self.assertEqual(ret, 1)
        self.assertEqual(len(stack), 3)
        self.assertEqual(stack[0], 24)
        self.assertEqual(stack[1], 44)
        self.assertEqual(stack[2], 78)
    
    def test_swap_throws(self):
        # Setup
        swap = Swap(1)
        stack = array(WORD_TYPE)
        
        # Run and Assert
        self.assertRaises(StackError, lambda: swap.execute(Runtime(stack)))


    def test_discard(self):
        # Setup
        discard = Discard(1)
        stack = array(WORD_TYPE)
        stack.append(24)
        stack.append(78)
        
        # Run
        ret = discard.execute(Runtime(stack))

        # Assert
        self.assertEqual(ret, 1)
        self.assertEqual(len(stack), 1)
        self.assertEqual(stack[0], 24)
    
    def test_discard_throws(self):
        # Setup
        discard = Discard(1)
        stack = array(WORD_TYPE)
        
        # Run and Assert
        self.assertRaises(StackError, lambda: discard.execute(Runtime(stack)))

    def test_plus(self):
        # Setup
        plus = Plus(1)
        stack = array(WORD_TYPE)
        stack.append(24)
        stack.append(78)
        
        # Run
        ret = plus.execute(Runtime(stack))

        # Assert
        self.assertEqual(ret, 1)
        self.assertEqual(len(stack), 1)
        self.assertEqual(stack[0], 24 + 78)

    def test_plus_throws(self):
        # Setup
        plus = Plus(1)
        stack = array(WORD_TYPE)
        stack.append(34) # need two for plus
        
        # Run and Assert
        self.assertRaises(StackError, lambda: plus.execute(Runtime(stack)))
    

    def test_minus(self):
        # Setup
        minus = Minus(1)
        stack = array(WORD_TYPE)
        stack.append(24)
        stack.append(78)
        
        # Run
        ret = minus.execute(Runtime(stack))

        # Assert
        self.assertEqual(ret, 1)
        self.assertEqual(len(stack), 1)
        self.assertEqual(stack[0], 24 - 78)

    def test_minus_throws(self):
        # Setup
        minus = Minus(1)
        stack = array(WORD_TYPE)
        stack.append(34) # need two for plus
        
        # Run and Assert
        self.assertRaises(StackError, lambda: minus.execute(Runtime(stack)))
    
    def test_times(self):
        # Setup
        times = Times(1)
        stack = array(WORD_TYPE)
        stack.append(8)
        stack.append(3)
        
        # Run
        ret = times.execute(Runtime(stack))

        # Assert
        self.assertEqual(ret, 1)
        self.assertEqual(len(stack), 1)
        self.assertEqual(stack[0], 24)

    def test_times_throws(self):
        # Setup
        times = Times(1)
        stack = array(WORD_TYPE)
        stack.append(34) # need two for plus
        
        # Run and Assert
        self.assertRaises(StackError, lambda: times.execute(Runtime(stack)))
    
    def test_int_divide(self):
        # Setup
        file = io.StringIO("")
        div = IntDivide(1)
        stack = array(WORD_TYPE)
        stack.append(10)
        stack.append(3)
        
        # Run
        ret = div.execute(Runtime(stack))

        # Assert
        self.assertEqual(ret, 1)
        self.assertEqual(file.getvalue(), "")
        self.assertEqual(len(stack), 1)
        self.assertEqual(stack[0], 3)

    def test_int_divide_throws(self):
        # Setup
        file = io.StringIO("")
        div = IntDivide(1)
        stack = array(WORD_TYPE)
        stack.append(34) # need two for div
        
        # Run and Assert
        self.assertRaises(StackError, lambda: div.execute(Runtime(stack)))
    

    def test_modulo(self):
        # Setup
        file = io.StringIO("")
        mod = Modulo(1)
        stack = array(WORD_TYPE)
        stack.append(10)
        stack.append(3)
        
        # Run
        ret = mod.execute(Runtime(stack))

        # Assert
        self.assertEqual(ret, 1)
        self.assertEqual(file.getvalue(), "")
        self.assertEqual(len(stack), 1)
        self.assertEqual(stack[0], 1)

    def test_mod_throws(self):
        # Setup
        file = io.StringIO("")
        mod = Modulo(1)
        stack = array(WORD_TYPE)
        stack.append(34) # need two for div
        
        # Run and Assert
        self.assertRaises(StackError, lambda: mod.execute(Runtime(stack)))

    def test_copy(self):
        # Setup
        file = io.StringIO("")
        copy = Copy(1, 2) # Copy 3rd entry from end of the stack
        stack = array(WORD_TYPE)
        stack = list(range(10, 20)) # Start stack with 10, 11, ... 19
        runtime = Runtime(stack)

        # Run
        ret = copy.execute(runtime)

        # Assert
        self.assertEqual(ret, 1)
        self.assertEqual(file.getvalue(), "")
        self.assertEqual(len(runtime.stack), 11)
        self.assertEqual(runtime.stack[-1], 17)


    def test_copy_throws(self):
        # Setup
        file = io.StringIO("")
        copy = Copy(1, 10) # Copy 11th entry from end of the stack
        stack = array(WORD_TYPE)
        stack = list(range(10, 20)) # Start stack with 10, 11, ... 19
        runtime = Runtime(stack)

        # Run, assert
        self.assertRaises(StackError, lambda: copy.execute(runtime))


    def test_slide(self):
        # Setup
        file = io.StringIO("")
        copy = Slide(1, 3) # Slide 3
        stack = array(WORD_TYPE)
        stack = list(range(10, 20)) # Start stack with 10, 11, ... 19
        runtime = Runtime(stack)

        # Run
        ret = copy.execute(runtime)

        # Assert
        self.assertEqual(ret, 1)
        self.assertEqual(file.getvalue(), "")
        self.assertEqual(len(runtime.stack), 7)
        self.assertEqual(runtime.stack, [10, 11, 12, 13, 14, 15, 19])


    def test_slide_throws(self):
        # Setup
        file = io.StringIO("")
        copy = Slide(1, 10) # Slide 10
        stack = array(WORD_TYPE)
        stack = list(range(10, 20)) # Start stack with 10, 11, ... 19
        runtime = Runtime(stack)

        # Run, assert
        self.assertRaises(StackError, lambda: copy.execute(runtime))


    ################
    # Control Flow #
    ################
    def test_end(self):
        # Setup
        file = io.StringIO("")
        end = End(1)
        stack = array(WORD_TYPE)
        
        # Run
        ret = end.execute(Runtime(stack))

        # Assert
        self.assertEqual(ret, -1)
        self.assertEqual(file.getvalue(), "")
        self.assertEqual(len(stack), 0)
    
    def test_callsub(self):
        # Setup
        callsub = CallSub(1, -1, 3) # Callsub to label 3
        callsub.target_pc = 12 # Suppose that label 3 points to instruction 12
        runtime = Runtime()
        runtime.PC = 8
        
        # Run
        ret = callsub.execute(runtime)

        # Assert
        self.assertEqual(ret, 12)
        self.assertEqual(len(runtime.callstack), 1)
        self.assertEqual(runtime.callstack[0], 8)
    
    def test_endsub(self):
        # Setup
        endsub = EndSub(1)
        runtime = Runtime()
        # print(runtime)
        runtime.callstack.append(12) # suppose last function call was from instruction 12
        # print(runtime)

        # Run
        ret = endsub.execute(runtime)

        # Assert
        self.assertEqual(ret, 12)
        self.assertEqual(len(runtime.callstack), 0)
    
    def test_jump(self):
        # Setup
        jump = Jump(1, -1, 123)
        jump.target_pc = 34
        runtime = Runtime()

        # Run
        ret = jump.execute(runtime)

        # Assert
        self.assertEqual(ret, 34)


    def test_jump_zero_doesnt_when_nonzero_stack_top(self):
        # Setup
        jumpZero = JumpZero(1, -1, 123)
        jumpZero.target_pc = 34
        runtime = Runtime()
        runtime.stack.append(2)

        # Run
        ret = jumpZero.execute(runtime)

        # Assert
        self.assertEqual(ret, 1)


    def test_jump_zero_jumps_when_zero_stack_top(self):
        # Setup
        jumpZero = JumpZero(1, -1, 123)
        jumpZero.target_pc = 34
        runtime = Runtime()
        runtime.stack.append(0)

        # Run
        ret = jumpZero.execute(runtime)

        # Assert
        self.assertEqual(ret, 34)


    def test_jump_zero_throws(self):
        # Setup
        jumpZero = JumpZero(1, -1, 123)
        jumpZero.target_pc = 34
        runtime = Runtime()

        # Run and assert
        self.assertRaises(StackError, lambda: jumpZero.execute(runtime))
    

    def test_jump_negative_doesnt_when_positive_stack_top(self):
        # Setup
        jumpNegative = JumpNegative(1, -1, 123)
        jumpNegative.target_pc = 34
        runtime = Runtime()
        runtime.stack.append(2)

        # Run
        ret = jumpNegative.execute(runtime)

        # Assert
        self.assertEqual(ret, 1)


    def test_jump_negative_jumps_when_neg1_stack_top(self):
        # Setup
        jumpNegative = JumpNegative(1, -1, 123)
        jumpNegative.target_pc = 34
        runtime = Runtime()
        runtime.stack.append(-1)

        # Run
        ret = jumpNegative.execute(runtime)

        # Assert
        self.assertEqual(ret, 34)


    def test_jump_negative_throws(self):
        # Setup
        jumpNegative = JumpNegative(1, -1, 123)
        jumpNegative.target_pc = 34
        runtime = Runtime()

        # Run and assert
        self.assertRaises(StackError, lambda: jumpNegative.execute(runtime))


    ########
    # Heap #
    ########
    def test_heap_read(self):
        # Setup
        readHeap = Read_Heap(1)
        stack = array(WORD_TYPE)
        stack.append(3)
        heap = Heap()
        heap.write(3, 123)

        # Run
        ret = readHeap.execute(Runtime(stack, heap))

        # Assert
        self.assertEqual(ret, 1)
        self.assertEqual(len(stack), 1)
        self.assertEqual(stack[0], 123)

    def test_heap_read_throws(self):
        # Setup
        heap_read = Read_Heap(1)
        stack = array(WORD_TYPE)
        heap = Heap()

        # Run and Assert
        self.assertRaises(StackError, lambda: heap_read.execute(Runtime(stack, heap)))
    
    def test_heap_write(self):
        # Setup
        writeHeap = Write_Heap(1)
        stack = array(WORD_TYPE)
        stack.append(3)
        stack.append(123)
        heap = Heap()

        # Run
        ret = writeHeap.execute(Runtime(stack, heap))

        # Assert
        self.assertEqual(ret, 1)
        self.assertEqual(len(stack), 0)
        self.assertEqual(heap.read(3), 123)

    def test_heap_write_throws(self):
        # Setup
        heap_write = Write_Heap(1)
        stack = array(WORD_TYPE)
        heap = Heap()

        # Run and Assert
        self.assertRaises(StackError, lambda: heap_write.execute(Runtime(stack, heap)))


if __name__ == "__main__":
    unittest.main()
