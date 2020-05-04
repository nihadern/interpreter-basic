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
from basic_program import ExpressionVisitor, Expression, StatementVisitor
from basic_program import Statement, Program
from typing import Union
from basic_tokens import Operators, Literals

"""
This file includes the interpreter class which is used to execute/interpret
a BASIC program using both the parser and scanner.
"""


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

    def __str__(self) -> str:
        """
        Returns an error message with details of the error.
        """
        return "InterpreterError: {}".format(self.err)


class Interpreter(StatementVisitor, ExpressionVisitor):
    def __init__(self, parser: Parser):
        self.parser = parser

    def interpret(self):
        """
        Interpreting involves retrieving the program from the parser and
        executing in a provided enviornment.
        """
        self.env = {}
        program = self.parser.program()
        for statement in program.statements:
            self.execute(statement)

    def execute(self, statement: Statement):
        """
        Executing a statement is visiting that statement.

        Arguments:
            statement {Statement} -- The statement to execute.
        """
        statement.accept(self)

    def evaluate(self, exp: Expression) -> Union[float, int]:
        """
        Evaluating an expression is visiting that expression.

        Arguments:
            exp {Expression} -- The expression to evaluate

        Returns:
            Union[float, int] -- depends on the value of the expression.
        """
        return exp.accept(self)

    def visit_binary(self, binary_exp: Expression.Binary) -> Union[float, int]:
        """
        Visit method for a binary expression.
        evaluating a binary expression returns the operator appplied to
        the evaluating left and right expression.

        Raises:
            InterpreterError: IF an invalid operator is found.

        Arguments:
            binary_exp {Expression.Binary} -- The binary expression visited.

        Returns:
            Union[float, int] -- depends on the value of the expressions.
        """
        l_expr = self.evaluate(binary_exp.l_expr)
        r_expr = self.evaluate(binary_exp.r_expr)
        if binary_exp.operator == Operators.ADD_OP:
            return l_expr + r_expr
        elif binary_exp.operator == Operators.SUB_OP:
            return l_expr - r_expr
        elif binary_exp.operator == Operators.MULT_OP:
            return l_expr * r_expr
        elif binary_exp.operator == Operators.DIV_OP:
            return l_expr / r_expr
        elif binary_exp.operator == Operators.EQUAL_OP:
            return bool(l_expr == r_expr)
        elif binary_exp.operator == Operators.GREATER_THAN:
            return bool(l_expr > r_expr)
        elif binary_exp.operator == Operators.LESS_THAN:
            return bool(l_expr < r_expr)
        elif binary_exp.operator == Operators.NOT_GREATER:
            return bool(l_expr <= r_expr)
        elif binary_exp.operator == Operators.NOT_LESS:
            return bool(l_expr >= r_expr)
        else:
            raise InterpreterError("Illegal operator found")

    def visit_unary(self, unary_exp: Expression.Unary) -> Union[float, int]:
        """
        Visit method for a unary expression.
        Evaluating a unary expression returns the operator applied to the
        value of the expression.

        Raises:
            InterpreterError: If an invalid operator is found

        Arguments:
            unary_exp {Expression.Unary} -- The unary expression visited.

        Returns:
            Union[float, int] -- depends on the value of the inner expression.
        """
        if unary_exp.operator == Operators.SUB_OP:
            return -self.evaluate(unary_exp.expr)
        elif unary_exp.operator == Operators.ADD_OP:
            return self.evaluate(unary_exp.expr)
        else:
            raise InterpreterError("Inavalid unary operator")

    def visit_literal(self,
                      literal_exp: Expression.Literal) -> Union[float, int]:
        """
        Visit method for a literal expression.
        Evaluating a literal returns the value of the literal.

        Arguments:
            literal_exp {Expression.Literal} -- The literal expression visited.

        Returns:
            Union[float, int] -- depends on the type of the literal.
        """
        return literal_exp.value

    def visit_grouping(self,
                       grouping_exp: Expression.Grouping) -> Union[float, int]:
        """
        Visit method for a grouping expression.
        The value of a grouping expression is the value evaluated
        expression inside.

        Arguments:
            grouping_exp {Expression.Grouping} -- The grouping expression
            visited.

        Returns:
            Union[float, int] -- depends on the value of the inner expression.
        """
        return self.evaluate(grouping_exp.expr)

    def visit_variable(self, variable_exp: Expression.Variable):
        """
        Visit method for a variable expression.
        The value of a variable expression returns the variable value
        in the enviornment

        Arguments:
            variable_exp {Expression.Variable} --  The variable expression
            visited.

        Returns:
            Union[float, int] -- depends on the value of the variable.
        """
        return self.env[variable_exp.identifier]

    def visit_assignment(self, assign_stmnt: Statement.Assignment):
        """
        Visit method for a assignment statement.
        Execution of an assignment sets the value of the variable to
        the value of the reslved expression in the enviornment.

        Arguments:
            assign_stmnt {Statement.Assignment} -- The assignment statement
            visited.
        """
        self.env[assign_stmnt.identifier] = self.evaluate(assign_stmnt.expr)

    def visit_print(self, print_stmnt: Statement.Print):
        """
        Visit method for a print statement.
        Executing a print statement prints the expression value to
        STDOUT.
        Arguments:
            print_stmnt {Statement.Print} -- The print statement visited.
        """
        print(self.evaluate(print_stmnt.expr))

    def visit_dowhile(self, dowhile_stmnt: Statement.DoWhile):
        """
        Visit method for a do while statement.
        Excecuting a DO WHILE loop executes all statements in the body
        while the relational expression is True.


        Arguments:
            dowhile_stmnt {Statement.DoWhile} -- The do while statement
            visited.
        """
        while self.evaluate(dowhile_stmnt.rel_expr):
            for statement in dowhile_stmnt.body:
                self.execute(statement)

    def visit_if(self, if_stmnt: Statement.If):
        """
        Visit method for an if statement.
        Excecuting an IF statement executes all statements in the body
        if the relational expression is True.

        Arguments:
            if_stmnt {Statement.If} -- The if statement visited.
        """
        if self.evaluate(if_stmnt.rel_expr):
            for statement in if_stmnt.body:
                self.execute(statement)

    def visit_end(self, end_stmnt: Statement.End):
        """
        Visit method for an end statement.
        Executing the end statement does nothing.

        Arguments:
            end_stmnt {Statement.End} -- The end statement visited.
        """
        pass


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
