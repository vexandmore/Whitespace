import sys
from whitespace.Runner import execute

def main() -> None:
    if len(sys.argv) >= 2:
        filename = sys.argv[1]
        with open(filename, "r", encoding="utf-8") as f:
            contents = f.read()
        execute(contents)

    else:
        print("ERROR: no file")

if __name__ == "__main__":
    main()
