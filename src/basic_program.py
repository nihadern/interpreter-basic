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
from basic_tokens import Operators, Literals, Identifiers, Tokens
from typing import Union
from abc import ABC, abstractmethod

"""
This file contains the code representation of a parse tree. This is
primarily used to communicate between the parser and the interpreter.
The tree is represented as classes which are meant to be nested.
"""


class ExpressionVisitor(ABC):
    """
    Abstract base class for a expression visitor following the visitor pattern.
    Acts as a contract for a concrete visitor class (like interpreter).

    Arguments:
        ABC {object} -- Used to define an abstract base class.
    """
    @abstractmethod
    def visit_binary(self, binary_exp):
        """
        Visit method for a binary expression.

        Arguments:
            binary_exp {Expression.Binary} -- The binary expression visited.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_unary(self, unary_exp):
        """
        Visit method for a unary expression.

        Arguments:
            unary_exp {Expression.Unary} -- The unary expression visited.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_literal(self, literal_exp):
        """
        Visit method for a literal expression.

        Arguments:
            literal_exp {Expression.Literal} -- The literal expression visited.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_grouping(self, grouping_exp):
        """
        Visit method for a grouping expression.

        Arguments:
            grouping_exp {Expression.Grouping} -- The grouping expression
            visited.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_variable(self, variable_exp):
        """
        Visit method for a variable expression.

        Arguments:
            variable_exp {Expression.Variable} --  The variable expression
            visited.
        """
        raise NotImplementedError


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

        def accept(self, visitor: ExpressionVisitor):
            return visitor.visit_literal(self)

    class Unary:
        """
        Encapsulates the operator and expression
        of the unary expression.
        """

        def __init__(self, operator: Operators, expr):
            super().__init__()
            self.operator = operator
            self.expr = expr

        def accept(self, visitor: ExpressionVisitor):
            return visitor.visit_unary(self)

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

        def accept(self, visitor: ExpressionVisitor):
            return visitor.visit_binary(self)

    class Grouping:
        """
        Encapsulates the expression inside a grouping expression.
        """

        def __init__(self, expr):
            super().__init__()
            self.expr = expr

        def accept(self, visitor: ExpressionVisitor):
            return visitor.visit_grouping(self)

    class Variable:
        """
        Encapsulates the identifer of a variable expression.
        """

        def __init__(self, identifier):
            super().__init__()
            self.identifier = identifier

        def accept(self, visitor: ExpressionVisitor):
            return visitor.visit_variable(self)


class StatementVisitor(ABC):

    @abstractmethod
    def visit_assignment(self, assign_stmnt):
        """
        Visit method for a assignment statement.

        Arguments:
            assign_stmnt {Statement.Assignment} -- The assignment statement
            visited.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_print(self, print_stmnt):
        """
        Visit method for a print statement.

        Arguments:
            print_stmnt {Statement.Print} -- The print statement visited.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_dowhile(self, dowhile_stmnt):
        """
        Visit method for a do while statement.

        Arguments:
            dowhile_stmnt {Statement.DoWhile} -- The do while statement
            visited.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_if(self, if_stmnt):
        """
        Visit method for an if statement.

        Arguments:
            if_stmnt {Statement.If} -- The if statement visited.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_end(self, end_stmnt):
        """
        Visit method for an end statement.

        Arguments:
            end_stmnt {Statement.End} -- The end statement visited.
        """
        raise NotImplementedError


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

        def accept(self, visitor: StatementVisitor):
            return visitor.visit_assignment(self)

    class Print:
        """
        Ecapsulates the expression of a print statement.
        """

        def __init__(self, expr: Expression):
            self.expr = expr

        def accept(self, visitor: StatementVisitor):
            return visitor.visit_print(self)

    class DoWhile:
        """
        Encapsulates the body and relational expression of a DO WHILE loop.
        """

        def __init__(self, rel_expr: Expression, body: list) -> None:
            self.rel_expr = rel_expr
            self.body = body

        def accept(self, visitor: StatementVisitor):
            return visitor.visit_dowhile(self)

    class If:
        """
        Encapsulates the body and relational expression of a IF statement.
        """

        def __init__(self, rel_expr: Expression, body: list):
            self.rel_expr = rel_expr
            self.body = body

        def accept(self, visitor: StatementVisitor):
            return visitor.visit_if(self)

    class End:
        """
        Placeholder for the END statement
        """

        def accept(self, visitor: StatementVisitor):
            return visitor.visit_end(self)


class Program:
    """
    Encapsulates the statements in a program.
    """

    def __init__(self, statements: list):
        self.statements = statements
