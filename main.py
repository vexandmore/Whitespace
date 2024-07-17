from whitespace.Runner import execute, minify
import sys
import os
from argparse import ArgumentParser, Namespace

def parse_args() -> Namespace:
    parser = ArgumentParser(description="Run whitespace interpreter/transformer")
    parser.add_argument('-l', dest='loose', metavar="loose", action="store_const", const=True, default=False)
    parser.add_argument('-m', dest='minify', metavar="minify", action="store_const", const=True, default=False)
    parser.add_argument('-p', dest='print', metavar="print", action="store_const", const=True, default=False)
    parser.add_argument('file', metavar='file', nargs=1, default=None, type=str)
    args = parser.parse_args(sys.argv[1:])

    print(f"Loose mode: {args.loose}, minify: {args.minify}, file to interpret: {args.file[0]}\n")

    return args


def main() -> None:
    args = parse_args()

    if len(args.file) > 0:
        filename = args.file[0]
        with open(filename, "r", encoding="utf-8") as f:
            contents = f.read()
        if args.minify:
            minified = minify(contents, args.loose)
            out_filename = os.path.splitext(filename)[0] + ".min.ws"
            with open(out_filename, "w", encoding="utf-8") as f:
                f.write(minified)
                print("Wrote minified file to " + out_filename)
        else:
            execute(contents, args.loose, args.print)

    else:
        print("ERROR: no file")

if __name__ == "__main__":
    main()
