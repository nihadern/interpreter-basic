"""
Python Implementation of a parse tree for a Subset of BASIC (ECMA 116 Standard)
Created by Nihad Kalathingal and Nick Green on 4/26/2020. Modified (04-30-2020)
    Kennesaw State University
    College of Computing and Software Engineering
    Department of Computer Science
    4308 Concepts of Programming Languages 03
    Module 8 – 3rd Deliverable
    Nihad Kalathingal (nkalathi@students.kennesaw.edu)
    Nick Green (ngreen@students.kennesaw.edu)
"""
from basic_subset import Operators, Literals, Identifiers, Tokens
from typing import Union
from abc import ABC, abstractmethod

"""
This file contains the code representation of a parse tree. This is
primarily used to communicate between the parser and the interpreter.
The tree is represented as classes which are meant to be nested.
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


class Expression:
    """
    Base class for expressions that includes all types of valid expressions
    in the subset. All subclasses include a resolve method which is used
    by the interreter to resolve expressions given an enviornment.

    Raises:
        InterpreterError: when resolving encounters an error
    """
    class Literal:
        """
        Literal expression which encapsulates the type and value of the
        a parser literal.
        """

        def __init__(self, type: Literals, value):
            super().__init__()
            self.type = type
            self.value = value

        def resolve(self, env: dict) -> Union[float, int]:
            """
            Resolving a literal returns the value of the literal.

            Arguments:
                env {dict} -- enviornment of the interpreter where variables
                are stored.

            Returns:
                Number -- a float or int is returned depending on the literal
            """
            return self.value

    class Unary:
        """
        Encapsulates the operator and expression
        of the unary expression.
        """

        def __init__(self, operator: Operators, expr):
            super().__init__()
            self.operator = operator
            self.expr = expr

        def resolve(self, env: dict) -> Union[float, int]:
            """
            Resolving a unary expression returns the operator applied to the
            value of the expressio.

            Arguments:
                env {dict} -- enviornment of the interpreter where variables
                are stored.

            Raises:
                InterpreterError: If an invalid operator is found

            Returns:
                Union[float, int] -- depends on the value of expression
            """
            if self.operator == Operators.SUB_OP:
                return -self.expr.resolve(env)
            elif self.operator == Operators.ADD_OP:
                return self.expr.resolve(env)
            else:
                raise InterpreterError("Inavalid unary operator")

    class Binary:
        """
        Ecapsulates the operator, right expression and left expression
        of a binary expression.
        """

        def __init__(self, l_expr, operator: Operators,
                     r_expr):
            super().__init__()
            self.l_expr = l_expr
            self.operator = operator
            self.r_expr = r_expr

        def resolve(self, env: dict) -> Union[float, int, bool]:
            """
            Resolving a binary expression returns the operator appplied to
            the resolved left and right expression.

            Arguments:
                env {dict} -- enviornment of the interpreter where variables
                are stored.

            Raises:
                InterpreterError: IF an invalid operator is found.

            Returns:
                Union[float, int, bool] -- depending on the operator and
                expression, a float, int, or boolean in returned.
            """
            l_expr = self.l_expr.resolve(env)
            r_expr = self.r_expr.resolve(env)
            if self.operator == Operators.ADD_OP:
                return l_expr + r_expr
            elif self.operator == Operators.SUB_OP:
                return l_expr - r_expr
            elif self.operator == Operators.MULT_OP:
                return l_expr * r_expr
            elif self.operator == Operators.DIV_OP:
                return l_expr / r_expr
            elif self.operator == Operators.EQUAL_OP:
                return bool(l_expr == r_expr)
            elif self.operator == Operators.GREATER_THAN:
                return bool(l_expr > r_expr)
            elif self.operator == Operators.LESS_THAN:
                return bool(l_expr < r_expr)
            elif self.operator == Operators.NOT_GREATER:
                return bool(l_expr <= r_expr)
            elif self.operator == Operators.NOT_LESS:
                return bool(l_expr >= r_expr)
            else:
                raise InterpreterError("Illegal operator found")

    class Grouping:
        """
        Encapsulates the expression inside a grouping expression.
        """

        def __init__(self, expr):
            super().__init__()
            self.expr = expr

        def resolve(self, env: dict) -> Union[float, int]:
            """
            The value of a grouping expression is the value resolved
            expression inside .

            Arguments:
                env {dict} -- enviornment of the interpreter where variables
                are stored.

            Returns:
                Union[float, int] -- depends on the value of expression
            """
            return self.expr.resolve(env)

    class Variable:
        """
        Encapsulates the identifer of a variable expression.
        """

        def __init__(self, identifier):
            super().__init__()
            self.identifier = identifier

        def resolve(self, env: dict) -> Union[float, int]:
            """
            The value of a variable expression returns the variable value
            in the enviornment

            Arguments:
                env {dict} -- enviornment of the interpreter where variables
                are stored.

            Returns:
                Union[float, int] -- depends on the value of the variable
            """
            return env[self.identifier]


class Statement:
    """
    Base class for all valid statements in the BASIC subset.
    """
    class Assignment:
        """
        Encapsulates the identifier and expression of the assignment statetment
        """

        def __init__(self, identifier: str, expr: Expression):
            self.identifier = identifier
            self.expr = expr

        def execute(self, env: dict) -> None:
            """
            Execution of an assignment sets the value of the variable to
            the value of the reslved expression in the enviornment.

            Arguments:
                env {dict} -- enviornment of the interpreter where variables
                are stored.
            """
            env[self.identifier] = self.expr.resolve(env)

    class Print:
        """
        Ecapsulates the expression of a print statement.
        """

        def __init__(self, expr: Expression):
            self.expr = expr

        def execute(self, env: dict) -> None:
            """
            Executing a print statement prints the expression value to
            STDOUT.

            Arguments:
                env {dict} -- enviornment of the interpreter where variables
                are stored.
            """
            print(self.expr.resolve(env))

    class DoWhile:
        """
        Encapsulates the body and relational expression of a DO WHILE loop.
        """

        def __init__(self, rel_expr: Expression, body: list) -> None:
            self.rel_expr = rel_expr
            self.body = body

        def execute(self, env: dict) -> None:
            """
            Excecuting a DO WHILE loop executes all statements in the body
            while the relational expression is True.

            Arguments:
               env {dict} -- enviornment of the interpreter where variables
                are stored.
            """
            while self.rel_expr.resolve(env):
                for statement in self.body:
                    statement.execute(env)

    class If:
        """
        Encapsulates the body and relational expression of a IF statement.
        """

        def __init__(self, rel_expr: Expression, body: list):
            self.rel_expr = rel_expr
            self.body = body

        def execute(self, env: dict) -> None:
            """"
            Excecuting an IF statement executes all statements in the body
            if the relational expression is True.

            Arguments:
               env {dict} - - enviornment of the interpreter where variables
                are stored.
            """
            if self.rel_expr.resolve(env):
                for statement in self.body:
                    statement.execute(env)

    class End:
        """
        Placeholder for the END statement
        """

        def execute(self, env: dict) -> None:
            """
            Executing the end statement does nothing.

            Arguments:
                env {dict} - - enviornment of the interpreter where variables
                are stored.
            """
            pass


class Program:
    """
    Encapsulates the statements in a program.
    """

    def __init__(self, statements: list):
        self.statements = statements

    def execute(self, env: dict) -> None:
        """
        Executing a program executes all of the statements in the program.

        Arguments:
            env {dict} - - enviornment of the interpreter where variables
                are stored.
        """
        for statement in self.statements:
            statement.execute(env)
