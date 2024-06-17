from whitespace.tokenizer import Tokenizer, Token, TokenType
from whitespace.parser import Command, Push, End, OutChar, Parser
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


if __name__ == "__main__":
    unittest.main()
