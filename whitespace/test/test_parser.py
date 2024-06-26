from whitespace.parser import Command, Push, End, OutChar, Parser, OutNum, ReadNum, ReadChar, Duplicate, Swap, Discard
from whitespace.parser import Plus, Minus, Times, IntDivide, Modulo, Write_Heap, Read_Heap
import unittest


class TestParser(unittest.TestCase):
    def run_test(self, source: str, expected: list[Command]) -> None:
        t = Parser(source)
        tokens = t.allCommands()
        self.assertEqual(len(expected), len(tokens), f"Check commands are right length: expect {expected}, {tokens}")
        for expected_t,actual_t in zip(expected, tokens):
            self.assertEqual(expected_t, actual_t)


    def test_1(self):
        self.run_test("[Tab][LF][Space][Space]", [OutChar(1)])
        self.run_test("[LF][LF][LF]", [End(1)])
        self.run_test("[Space][Space]Push[Space]+[Tab][Space]" +
                      "[Space][Tab][Space][Space][Space][LF]", [Push(1, 72)])
        self.run_test("[Space][Space]Push[Space]+[Tab][Space]" +
                      "[Space][Tab][Space][Space][Space][LF]\n" +
                      "[Tab][LF][Space][Space]\n" + 
                      "[LF][LF][LF]", [Push(1, 72), OutChar(2), End(3)])
    
    def test_io(self):
        self.run_test("[Tab][LF][Space][Space]", [OutChar(1)])
        self.run_test("[Tab][LF][Space][Tab]", [OutNum(1)])
        self.run_test("[Tab][LF][Tab][Space]", [ReadChar(1)])
        self.run_test("[Tab][LF][Tab][Tab]", [ReadNum(1)])


        self.run_test("[Tab][LF][Space][Space][Tab][LF][Space]" + 
                      "[Tab][Tab][LF][Tab][Space][Tab][LF][Tab][Tab]",
                      [OutChar(1), OutNum(1), ReadChar(1), ReadNum(1)])

    def test_stack_manip(self):
        self.run_test("[Space][LF][Space]", [Duplicate(1)])
        self.run_test("[Space][LF][Tab]", [Swap(1)])
        self.run_test("[Space][LF][LF]", [Discard(1)])

        
        self.run_test("[Tab][LF][Space][Space][Space][LF][Space]",
                [OutChar(1), Duplicate(1)])
        self.run_test("[Space][LF][Tab][Space][LF][LF][Tab][LF][Space][Space][Space][LF][Space]",
                [Swap(1), Discard(1), OutChar(1), Duplicate(1)])

    def test_arithmetic(self):
        self.run_test("\n[Tab][Space][Space][Space]", [Plus(2)])
        self.run_test("\n\n\n[Tab][Space][Space][Tab]", [Minus(4)])
        self.run_test("[Tab][Space][Space][LF]", [Times(1)])
        self.run_test("\n[Tab][Space][Tab][Space]", [IntDivide(2)])
        self.run_test("\n\n[Tab][Space][Tab][Tab]", [Modulo(3)])

        self.run_test("[Tab][Space][Space][Space]\n"
                    + "[Tab][Space][Space][Tab]\n"
                    + "[Tab][Space][Space][LF]\n"
                    + "[Tab][Space][Tab][Space]\n"
                    + "[Tab][Space][Tab][Tab]", 
                    [Plus(1), Minus(2), Times(3), IntDivide(4), Modulo(5)])

    def test_heap(self):
        self.run_test("\n[Tab][Tab][Space]", [Write_Heap(2)])
        self.run_test("\n\n[Tab][Tab][Tab]", [Read_Heap(3)])

        self.run_test("[Tab][Space][Space][Space]\n"
                    + "[Tab][Space][Space][Tab]\n"
                    + "[Tab][Tab][Space]\n"
                    + "[Tab][Tab][Tab]",
                    [Plus(1), Minus(2), Write_Heap(3), Read_Heap(4)])
    

    def test_labels(self):
        self.run_test("[LF][Space][Space][Tab][Tab][LF]Label 3 [Tab][Tab][Space]", [Write_Heap(1, 3)])
        self.run_test("[LF][Space][Space][Tab][Tab][LF]Label 3 [Tab][LF][Space][Space]", [OutChar(1, label=3)])
        self.run_test("[LF][Space][Space][Tab][Tab][LF]Label 3 [LF][LF][LF]", [End(1, 3)])
        self.run_test("[LF][Space][Space][Tab][Tab][LF]Label 3" +
                    "[Space][Space]Push[Space]+[Tab][Space]" +
                      "[Space][Tab][Space][Space][Space][LF]", [Push(1,72,3)])


if __name__ == "__main__":
    unittest.main()
