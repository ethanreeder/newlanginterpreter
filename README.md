# newlanginterpreter

Interpreter for a novel simple programming language. Syntax is detailed in syntax.txt.

Run from top level directory on file 'file.txt' as follows:

> python3 interpreter.py -f file.txt

Result is printed to stdout.

Includes:
 - An abstract syntax tree of the novel language
 - Parsing from JSON to python readable format
 - A full interpreter for the language
 - Comprehensive errors
 - Easily expandable parser and interpreter context for tracking function and variable declarations

Future plans:
 - Code structure for variable definition and access exists, and it would be fun to add that!
 - Context could also include a parsing and interpreting traceback which would make it feel like a real interpreter
 - Add other flags such as verbosity for detailed information while parsing or interpreting
 - Add simple terminal shell for easy testing
 - Could easily add simple lexer in the place of python's JSON library

Issues:
 - bugs with evaluating functions
 - test cases or test syntax files not included
 - unittest module had issues with python enum (but would have been very time intensive to create with 3 hr constraint)
