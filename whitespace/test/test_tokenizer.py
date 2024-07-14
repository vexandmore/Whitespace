from whitespace.Tokenizer import Tokenizer, Token, TokenType
import unittest


class TestToken(unittest.TestCase):
    def test_fromString(self):
        self.assertEqual(TokenType.SPACE, TokenType.fromString(" "))
        self.assertEqual(TokenType.TAB, TokenType.fromString("\t"))
        self.assertEqual(TokenType.LINEFEED, TokenType.fromString("\n"))


class TestTokenizer(unittest.TestCase):
    def run_test(self, source: str, expected: list[TokenType]) -> None:
        t = Tokenizer(source)
        tokens = t.allTokens()
        self.assertEqual(len(expected), len(tokens), "Check tokens are right length")
        for expected_t,actual_t in zip(expected, tokens):
            self.assertEqual(expected_t, actual_t)

    def test_normal_mode(self):
        self.run_test(" ", [Token(TokenType.SPACE, 1)])
        self.run_test(" \t", [Token(TokenType.SPACE, 1),Token(TokenType.TAB, 1)])
        self.run_test(" \t\n  \t \n", 
                      [Token(TokenType.SPACE, 1),Token(TokenType.TAB, 1), Token(TokenType.LINEFEED, 1),
                       Token(TokenType.SPACE, 2), Token(TokenType.SPACE, 2), Token(TokenType.TAB, 2), Token(TokenType.SPACE, 2), Token(TokenType.LINEFEED, 2)])
        
        self.run_test(" \t\n asdhco384 \tdfsd3 \n3343", 
                      [Token(TokenType.SPACE, 1),Token(TokenType.TAB, 1), Token(TokenType.LINEFEED, 1),
                       Token(TokenType.SPACE, 2), Token(TokenType.SPACE, 2), Token(TokenType.TAB, 2), Token(TokenType.SPACE, 2), Token(TokenType.LINEFEED, 2)])
        
    def test_readable_mode(self):
        self.run_test("[Space]", [Token(TokenType.SPACE, 1)])
        self.run_test("[Space][Tab]", [Token(TokenType.SPACE, 1),Token(TokenType.TAB, 1)])
        self.run_test("[Space][Tab][LF]\n[Space][Space][Tab][Space][LF]", 
                      [Token(TokenType.SPACE, 1),Token(TokenType.TAB, 1), Token(TokenType.LINEFEED, 1),
                       Token(TokenType.SPACE, 2), Token(TokenType.SPACE, 2), Token(TokenType.TAB, 2), Token(TokenType.SPACE, 2), Token(TokenType.LINEFEED, 2)])
        
        self.run_test("[Space][Tab][LF]\n[Space]asdhco384[Space][Tab]dfsd3[Space][LF]\n3343", 
                      [Token(TokenType.SPACE, 1),Token(TokenType.TAB, 1), Token(TokenType.LINEFEED, 1),
                       Token(TokenType.SPACE, 2), Token(TokenType.SPACE, 2), Token(TokenType.TAB, 2), Token(TokenType.SPACE, 2), Token(TokenType.LINEFEED, 2)])

        self.run_test("[Space][Space]Push[Space]+[Tab][Space]" +
                      "[Space][Tab][Space][Space][Space][Space][LF]",
                      [Token(TokenType.SPACE, 1), Token(TokenType.SPACE, 1),
                       Token(TokenType.SPACE, 1), Token(TokenType.TAB, 1),
                       Token(TokenType.SPACE, 1), Token(TokenType.SPACE, 1),
                       Token(TokenType.TAB, 1), Token(TokenType.SPACE, 1),
                       Token(TokenType.SPACE, 1), Token(TokenType.SPACE, 1),
                       Token(TokenType.SPACE, 1), Token(TokenType.LINEFEED, 1)])
        

if __name__ == "__main__":
    unittest.main()
