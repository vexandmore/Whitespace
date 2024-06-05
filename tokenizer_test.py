from whitespace import Tokenizer, Token, TokenType
import unittest

class TestTokenizer(unittest.TestCase):
    def test_normal_mode(self):
        t = Tokenizer("   \t\n")
        tokens = t.allTokens()
        self.assertEqual(tokens[0], Token(TokenType.SPACE, 1))
