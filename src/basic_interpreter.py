"""
Python Implementation of a Interpreter for a Subset of BASIC (ECMA 116 Standard)
Created by Nihad Kalathingal and Nick Green on 4/26/2020. Modified (04-26-2020)
    Kennesaw State University
    College of Computing and Software Engineering
    Department of Computer Science
    4308 Concepts of Programming Languages 03
    Module 8 – 3rd Deliverable
    Nihad Kalathingal (nkalathi@students.kennesaw.edu)
    Nick Green (ngreen@students.kennesaw.edu)
"""
# import scanner and scanner errors
from basic_scanner import Scanner, ScannerError
import sys  # import sys used for CLI args
from basic_parser import ParserError, Parser

"""
This file includes the interpreter class which is used to execute/interpret 
a BASIC program using both the parser and scanner.
"""


class Interpreter:
    """
    Interpreter which uses the parser in order to execute a BASIC program.
    """

    def __init__(self, parser: Parser):
        self.parser = parser

    def interpret(self):
        """
        Interpreting involves retrieving the program from the parser and 
        executing in a provided enviornment. 
        """
        self.env = {}
        program = self.parser.program()
        program.execute(self.env)


def main():
    '''
    Ensure that the Python 3 interpreter is installed.
    The interpreter can be used with BASIC file using the following command:

    python3 basic_interpreter.py <filename>

    For example:

    python3 basic_interpreter.py test.bas

    Ensure that the file is in the same folder as the script or provide an
    a path to file.
    '''
    # get the filename from the first CLI argument
    filename = sys.argv[1]
    # use with context manager to open/close file and use
    # exception handling
    with open(filename, "r") as f:
        scanner = Scanner(f)  # create a scanner object with a source file
        # make the generator global to be used with parser functions
        # initialize parser with scanner
        parser = Parser(scanner)
        # initialize interpreter with parser
        interpreter = Interpreter(parser)
        # try catch to catch any parser errors
        try:
            # start interpreting the program
            interpreter.interpret()
        except ParserError as e:
            # if a parsing error occurred, alert the user
            print(e)
        except ScannerError as e:
            # if a scanning error occurred, alert the user
            print(e)
        except Exception as e:
            # print any other errors
            print("Uknown Error Occured!")
            print(e)


if __name__ == "__main__":
    main()
