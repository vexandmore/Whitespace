# Summary
This is a [Whitespace](https://esolangs.org/wiki/Whitespace) interpreter in Python.
Currently, Whitespace 0.3 instructions are not implemented; will be done soon.
Written as a personal exercise in Python project structures, unit testing, 
and (soon TM) assembly code generation.

Python 3.10+ required for the type hints.

## Details

### Whitespace Syntax Information
If `-l` is passed, the input file can either be in the original input format (only
tabs, spaces, linefeeds are interpreted) or in a "readable mode" where [Space],
[Tab], [LF] are used instead. When readable mode is detected, actual whitespace is ignored.
Readable mode is detected when at least one of [Space], [Tab], or [LF] is detected in the file
(and this switch is passed).

### I/O Considerations
In Whitespace, there is no way to receive input other than stdin
(and no way to output except stdout). This interpreter does not address this currently.
In addition, some programs may expect to see a null (aka '\0')
when input is done; to input this, enter ctrl-C when the program is waiting
for input (if ctrl-c is entered at any another time, the program will quit).

### Word Size
Integers are twos complement 32-bit integers (stored in a python
as an array('l') to save space in memory).

### Dependencies
`nasm` and `ld` are needed for compiling. Note that the assembly generator
is only designed for AMD64 (Intel/AMD 64-bit) Linux systems, and is not tested on 
any other platforms.

# Usage
main.py [-h] [-l] [-m] [-p] [-v] [-c] file

## Primary Actions
Only one of these actions will be executed. By default, the file will be interpreted
and executed.

If `-m` is passed, the input file is minified (and transformed from readable mode
into pure whitespace if necessary) and written to a file with the same name as the
original, with a `.min.ws` extension (replacing whatever extension the original had).
The file is not run in this case.

If `-c` is passed, the input file will be compiled. The output name is currently
fixed to be the same as the input filename, but with no extension. 

## Other Options
If `-p` is passed, the program instructions will be outputed to the console 
before the file is interpreted.

If `-l` is passed, the input file can either be in the original input format or
in "readable mode" (see above).

If `-v` is passed, every executed instruction will be printed
out before it is executed (if the file is interpreted).

# Getting Started
To run whitespace file (in either syntax):
`python main.py -l examples/hello-world.ws`

# Tests
To run unit tests, from the root folder, run `python -m unittest`