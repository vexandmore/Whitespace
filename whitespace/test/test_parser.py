from whitespace.tokenizer import Tokenizer, Token, TokenType
from whitespace.parser import Command, OutChar, End, Push, Parser
import unittest


class TestToken(unittest.TestCase):
    def test_fromString(self):
        self.assertEqual(TokenType.SPACE, TokenType.fromString(" "))
        self.assertEqual(TokenType.TAB, TokenType.fromString("\t"))
        self.assertEqual(TokenType.LINEFEED, TokenType.fromString("\n"))


class TestTokenizer(unittest.TestCase):
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
        


if __name__ == "__main__":
    unittest.main()
