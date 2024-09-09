from whitespace.Heap import Heap
from whitespace.Constants_errors import HeapError
import unittest


class TestHeap(unittest.TestCase):
    def test_read(self):
        heap = Heap()

        heap.write(0, 123)
        heap.write(10, 456)
        heap.write(11, 789)
        
        self.assertEqual(123, heap.read(0))
        self.assertEqual(456, heap.read(10))
        self.assertEqual(789, heap.read(11))
    
    def test_growing(self):
        heap = Heap()

        heap.write(0, 123)
        heap.write(10, 456)
        heap.write(100, 789)
        heap.write(1000, 234)
        heap.write(10000, 567)
        heap.write(100000, 890)
        heap.write(1000000, 111)
        
        
        self.assertEqual(123, heap.read(0))
        self.assertEqual(456, heap.read(10))
        self.assertEqual(789, heap.read(100))
        self.assertEqual(234, heap.read(1000))
        self.assertEqual(567, heap.read(10000))
        self.assertEqual(890, heap.read(100000))
        self.assertEqual(111, heap.read(1000000))
        

    def test_read_0_on_read_past_end(self):
        heap = Heap()

        # Read null when not written
        self.assertEqual(0, heap.read(0))
        self.assertEqual(0, heap.read(12))

