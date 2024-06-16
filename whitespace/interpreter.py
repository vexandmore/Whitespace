import unittest
from whitespace.tokenizer import Tokenizer
from whitespace.tests.tokenizer_test import TestTokenizer
import sys


def main():
    with open("text.txt", mode="r") as f:
        source = f.read()
    


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[2] == "test":
        unittest.main()
    main()
