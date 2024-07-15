## Summary
This is a [Whitespace](https://esolangs.org/wiki/Whitespace) interpreter in Python.
Written as a personal exercise in Python project structures, unit testing, 
and (eventually) (possibly) assembly code generation or JITing.
Python 3.10+ required for the type hints.

## Syntax Information
If `-l` is passed, the input file can either be in the original input format (only
tabs, spaces, linefeeds are interpreted) or in a "readable mode" where [Space],
[Tab], [LF] are used instead (when readable mode is detected, actual whitespace is ignored).
Readable mode is detected when [Space], [Tab], and [LF] are all detected in the file.

If `-t` is passed, the input file is minified (and transformed from readable mode
into pure whitespace if necessary) and written to a file with the same name as the
original, with a `.min.ws` extension. The file is not run in this case.

If `-p` is passed, the program instructions will be outputed to the console 
before the file is interpreted.

## Getting Started
To run whitespace file (in either syntax):
`python main.py -l examples/hello-world.ws`

## Tests
To run unit tests, from the root folder, run `python -m unittest`