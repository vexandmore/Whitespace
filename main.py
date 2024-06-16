from whitespace.parser import Parser
import sys
from array import array

def main() -> None:
    if len(sys.argv) >= 2:
        filename = sys.argv[1]
        with open(filename, "r", encoding="utf-8") as f:
            contents = f.read()
        p = Parser(contents)
        program = p.allCommands()

        stack = array('b')
        heap: dict[int, int] = {}

        # No flow control yet
        for statement in program:
            statement.execute(stack, heap)

    else:
        print("ERROR: no file")

if __name__ == "__main__":
    main()
