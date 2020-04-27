from basic_subset import Operators, Literals, Identifiers, Tokens
from typing import Union


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


class Factor:
    def __init__(self, type, value: str):
        self.type = type
        self.value = value

    def resolve(self, env: dict) -> Union[float, int]:
        if self.type == Literals.INT_LIT:
            return int(self.value)
        elif self.type == Literals.FLOAT_LIT:
            return float(self.value)
        elif self.type == Identifiers.IDENT:
            try:
                return env[self.value]
            except KeyError:
                raise InterpreterError(
                    "{} used before assignment".format(self.value))
        else:
            return self.value.resolve(env)


class Term:
    def __init__(self, factor: Factor, operator: Operators, term):
        self.factor = factor
        self.operator = operator
        self.term = term

    def resolve(self, env: dict) -> Union[float, int]:
        factor_val = self.factor.resolve(env)
        if self.operator:
            if self.operator == Operators.MULT_OP:
                return factor_val * self.term.resolve(env)
            elif self.operator == Operators.DIV_OP:
                return factor_val / self.term.resolve(env)
            else:
                raise InterpreterError("Invalid operator in expression")
        else:
            return factor_val


class Expression:
    def __init__(self, operator: Operators, term: Term, expr):
        self.operator = operator
        self.term = term
        self.expr = expr

    def resolve(self, env: dict) -> Union[float, int]:
        term_val = self.term.resolve(env)
        if self.operator:
            if self.operator == Operators.ADD_OP:
                return term_val + self.expr.resolve(env)
            elif self.operator == Operators.SUB_OP:
                return term_val - self.expr.resolve(env)
            else:
                raise InterpreterError("Invalid operator in expression")
        else:
            return term_val


class RelationalExpression:
    def __init__(self, l_exp: Expression, operator: Operators,
                 r_exp: Expression):
        self.l_exp = l_exp
        self.r_exp = r_exp
        self.operator = operator

    def resolve(self, env: dict) -> bool:
        if self.operator == Operators.EQUAL_OP:
            return bool(self.l_exp.resolve(env) == self.r_exp.resolve(env))
        elif self.operator == Operators.LESS_THAN:
            return bool(self.l_exp.resolve(env) < self.r_exp.resolve(env))
        elif self.operator == Operators.GREATER_THAN:
            return bool(self.l_exp.resolve(env) > self.r_exp.resolve(env))
        elif self.operator == Operators.NOT_GREATER:
            return bool(self.l_exp.resolve(env) <= self.r_exp.resolve(env))
        elif self.operator == Operators.NOT_LESS:
            return bool(self.l_exp.resolve(env) >= self.r_exp.resolve(env))


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
        def __init__(self, rel_expr: RelationalExpression, body: list) -> None:
            self.rel_expr = rel_expr
            self.body = body

        def execute(self, env: dict) -> None:
            while self.rel_expr.resolve(env):
                for statement in self.body:
                    statement.execute(env)

    class If:
        def __init__(self, rel_expr: RelationalExpression, body: list):
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
