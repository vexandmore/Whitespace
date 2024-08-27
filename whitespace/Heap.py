from whitespace.Constants_errors import WORD_TYPE, HeapError
from array import array

class Heap:
    def __init__(self):
        self.arr = array(WORD_TYPE, [0, 0, 0, 0])
        # Maximum address written to. Used to return an error
        # if tring to read way past what's been written to before.
        self.max_written = -1

    def read(self, address: int) -> int:
        if address <= self.max_written:
            return self.arr[address]
        else:
            # Double size, and recurse
            self.arr.extend([0] * len(self.arr))
            return self.read(address)
    
    def write(self, address: int, value: int) -> None:
        if address > self.max_written:
            self.max_written = address

        if address < len(self.arr):
            self.arr[address] = value
        else:
            # Double size, and recurse
            self.arr.extend([0] * len(self.arr))
            self.write(address, value)
    
    def __repr__(self) -> str:
        return f"Heap {self.arr}, max addr is {self.max_written}"