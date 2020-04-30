from basic_subset import Operators, Literals, Identifiers, Tokens
from typing import Union
from abc import ABC, abstractmethod


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
    class Literal:

        def __init__(self, type: Literals, value):
            super().__init__()
            self.type = type
            self.value = value

        def resolve(self, env):
            return self.value

    class Unary:
        def __init__(self, operator: Operators, expr):
            super().__init__()
            self.operator = operator
            self.expr = expr

        def resolve(self, env):
            if self.operator == Operators.SUB_OP:
                return -self.expr.resolve(env)
            elif self.operator == Operators.ADD_OP:
                return self.expr.resolve(env)
            else:
                raise InterpreterError("Inavalid unary operator")

    class Binary:
        def __init__(self, l_expr, operator: Operators,
                     r_expr):
            super().__init__()
            self.l_expr = l_expr
            self.operator = operator
            self.r_expr = r_expr

        def resolve(self, env):
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
        def __init__(self, expr):
            super().__init__()
            self.expr = expr

        def resolve(self, env):
            return self.expr.resolve(env)

    class Variable:
        def __init__(self, identifier):
            super().__init__()
            self.identifier = identifier

        def resolve(self, env):
            return env[self.identifier]


class Statement:
    class Assignment:
        def __init__(self, identifier: str, expr: Expression):
            self.identifier = identifier
            self.expr = expr

        def execute(self, env: dict) -> None:
            env[self.identifier] = self.expr.resolve(env)

    class Print:
        def __init__(self, expr: Expression):
            self.expr = expr

        def execute(self, env: dict) -> None:
            print(self.expr.resolve(env))

    class DoWhile:
        def __init__(self, rel_expr: Expression, body: list) -> None:
            self.rel_expr = rel_expr
            self.body = body

        def execute(self, env: dict) -> None:
            while self.rel_expr.resolve(env):
                for statement in self.body:
                    statement.execute(env)

    class If:
        def __init__(self, rel_expr: Expression, body: list):
            self.rel_expr = rel_expr
            self.body = body

        def execute(self, env: dict):
            if self.rel_expr.resolve(env):
                for statement in self.body:
                    statement.execute(env)

    class End:
        def execute(self, env: dict):
            pass


class Program:
    def __init__(self, statements: list):
        self.statements = statements

    def execute(self, env: dict) -> None:
        for statement in self.statements:
            statement.execute(env)
