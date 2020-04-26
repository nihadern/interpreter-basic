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

from basic_scanner import *   # import scanner and scanner errors
from basic_subset import *  # import the basic subset with the tokens
import sys  # import sys used for CLI args
from basic_parser import *


class InterpreterError(Exception):
    """
    Exception class for a Interpreter error.
    Used in case a Interpreter error occurs.
    """

    def __init__(self, err=None):
        """
        Simple constructor to assign InterpreterError attributes.

        Parameters:
        pos (tuple): tuple of length 2 of the form (row, column)
        pos (str): string description of an error, a generic error is used
        if none is given
        """

        if err is None:
            # use a default error if none specified
            err = "Interpreter error occured."
        self.err = err

    def __str__(self):
        """
        Returns an error message with details of the error.
        """
        return "InterpreterError: {}".format(self.err)


class Interpreter:
    def __init__(self, parser: Parser):
        self.parser = parser

    def interpret(self):
        self.env = {}
        program = self.parser.program()
        for statement in program.statements:
            self.execute_statement(statement)

    def execute_statement(self, statement: Statement):
        if isinstance(statement, Statement.Print):
            self.execute_print(statement)
        elif isinstance(statement, Statement.Assignment):
            self.execute_assign(statement)
        elif isinstance(statement, Statement.DoWhile):
            self.execute_dowhile(statement)
        elif isinstance(statement, Statement.If):
            self.execute_if(statement)
        elif isinstance(statement, Statement.End):
            pass

    def execute_print(self, statement: Statement.Print):
        value = self.resolve_exp(statement.expr)
        print(value)

    def execute_assign(self, statement: Statement.Assignment):
        pass

    def execute_dowhile(self, statement: Statement.DoWhile):
        pass

    def execute_if(self, statement: Statement.If):
        pass

    def resolve_exp(self, exp: Expression):
        term_val = self.resolve_term(exp.term)
        if exp.operator:
            if exp.operator == Operators.ADD_OP:
                return term_val + self.resolve_exp(exp.expr)
            elif exp.operator == Operators.SUB_OP:
                return term_val - self.resolve_exp(exp.expr)
            else:
                raise InterpreterError("Invalid operator in expression")
        else:
            return term_val

    def resolve_term(self, term: Term):
        factor_val = self.resolve_factor(term.factor)
        if term.operator:
            if term.operator == Operators.MULT_OP:
                return factor_val * self.resolve_term(term.term)
            elif term.operator == Operators.DIV_OP:
                return factor_val / self.resolve_term(term.term)
            else:
                raise InterpreterError("Invalid operator in expression")
        else:
            return factor_val

    def resolve_factor(self, factor: Factor):
        if factor.type == Literals.INT_LIT:
            return int(factor.value)
        elif factor.type == Literals.FLOAT_LIT:
            return float(factor.value)
        elif factor.type == Identifiers.IDENT:
            try:
                return self.env[factor.value]
            except KeyError:
                raise ParserError(
                    "{} used before assignment".format(factor.value))
        else:
            return self.resolve_exp(factor.value)


def main():
    '''
    Ensure that the Python 3 interpreter is installed.
    The parser can be used with BASIC file using the following command:

    python3 parser.py <filename>

    For example:

    python3 parser.py test.bas

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
        parser = Parser(scanner)
        interpreter = Interpreter(parser)
        # try catch to catch any parser errors
        try:
            # start interpreting the program
            interpreter.interpret()
        except ParserError as e:
            # if a parsing error occurred, alert the user
            print(e)
        except Exception as e:
            # print any other errors
            print(e)


if __name__ == "__main__":
    main()
