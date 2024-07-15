from whitespace.Runner import execute
import sys
from argparse import ArgumentParser, Namespace

def parse_args() -> Namespace:
    parser = ArgumentParser(description="Run whitespace interpreter/transformer")
    parser.add_argument('-l', dest='loose', metavar="loose", action="store_const", const=True, default=False)
    parser.add_argument('-t', dest='transpile', metavar="transpile", action="store_const", const=True, default=False)
    parser.add_argument('file', metavar='file', nargs=1, default=None, type=str)
    args = parser.parse_args(sys.argv[1:])

    return args


def main() -> None:
    args = parse_args()

    if len(args.file) > 0:
        filename = args.file[0]
        with open(filename, "r", encoding="utf-8") as f:
            contents = f.read()
        execute(contents, args.loose)

    else:
        print("ERROR: no file")

if __name__ == "__main__":
    main()
