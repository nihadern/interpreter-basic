"""
Python Implementation of a Parser for a Subset of BASIC (ECMA 116 Standard)
Created by Nihad Kalathingal and Nick Green on 3/19/2020. Modified (03-20-2020)
    Kennesaw State University
    College of Computing and Software Engineering
    Department of Computer Science
    4308 Concepts of Programming Languages 03
    Module 3 – 2nd Deliverable
    Nihad Kalathingal (nkalathi@students.kennesaw.edu)
    Nick Green (ngreen@students.kennesaw.edu)
"""

from basic_scanner import *   # import scanner and scanner errors
from basic_subset import *  # import the basic subset with the tokens
import sys  # import sys used for CLI args
from basic_program import *
"""
The parser is implemented as functions which uses the BNF grammar rules
specified for the chosen Basic subset. The implementation is direct
in the sense that each non-terminal in the grammar has a function.
The parser uses the scanner to retrieve tokens specified by the Token
in the lex() function. The parser throws a ParserError if an invalid
statment is found.
"""


class ParserError(Exception):
    """
    Exception class for a Parser error.
    Used in case a parsing error occurs.
    """

    def __init__(self, pos: tuple, err=None):
        """
        Simple constructor to assign ParserError attributes.

        Parameters:
        pos (tuple): tuple of length 2 of the form (row, column)
        pos (str): string description of an error, a generic error is used
        if none is given
        """

        if err is None:
            # use a default error if none specified
            err = "Parsing error occured."
        self.err = err
        self.pos = pos  # position of error

    def __str__(self):
        """
        Returns an error message with details of the error.
        """
        return "ParserError: {} Ln:{} Col:{}".format(self.err, self.pos[0],
                                                     self.pos[1])


class Parser:
    def __init__(self, scanner):
        """
        Simple constructor to initialize next_token and lexer.
        """
        self.next_token = None
        self.lexer = scanner.lex()
        self.scanner = scanner

    def program(self):
        """
        Starting point for the parser.
        Function for the program non-terminal following the BNF rule:
        <program> -> <statements>
        """
        # enter program
        # print("<program>")
        # parse statements
        statements = self.statements()
        return Program(statements)
        # exit program
        # print("</program>")

    def statements(self):
        """
        Function for the statements non-terminal following the BNF rule:
        <statements> -> <statement>
                      | <statement> EOL <statements>
        """
        # parse statemnt
        self.lex()
        statements = []
        statements.append(self.statement())
        # while mext token EOL parse statements
        if self.next_token.type == Delimiters.EOL:
            statements = statements + self.statements()
        return statements

    def statement(self):
        """
        Function for the statement non-terminal following the BNF rule:
        <statement> -> <assn_stmnt>
                    | <print_stmnt>
                    | <do_while>
                    | <if_stmnt>
                    | END
        """
        # enter statement
        # print("<statement>")
        # choose type of statement based on next_token
        statement = None
        if self.next_token.type == Keywords.LET:
            statement = self.assn_stmnt()
        elif self.next_token.type == Keywords.PRINT:
            statement = self.print_stmnt()
        elif self.next_token.type == Keywords.DO:
            statement = self.do_while()
        elif self.next_token.type == Keywords.IF:
            statement = self.if_stmnt()
        elif self.next_token.type == Keywords.END:
            statement = Statement.End()
            #  empty statement/line, do nothing
        elif self.next_token.type == Delimiters.EOL:
            statement = Statement.End()
            #  empty statement/line, do nothing
        else:
            # raise a parsing error as its not a valid statement
            raise ParserError(self.next_token.pos,
                              "Invalid type of statement")
        # exit statement
        # print("</statement>")
        return statement

    def assn_stmnt(self):
        """
        Function for the assn_stmnt non-terminal following the BNF rule:
        <assn_stment> -> LET IDENT EQUAL_OP <expr>
        """
        # enter assig_stmnt
        # print("<assn_stmnt>")
        # check for identifier
        self.lex()
        identifier = self.next_token.lexeme
        if self.next_token.type != Identifiers.IDENT:
            raise ParserError(self.next_token.pos,
                              "Invalid identifier in assignment statement")
        # check for assinment operator
        self.lex()
        if self.next_token.type != Operators.EQUAL_OP:
            raise ParserError(self.next_token.pos,
                              "Invalid assignment statement")
        # parse an expression
        expression = self.expr()

        # exit assig_stmnt
        # print("</assn_stmnt>")
        return Statement.Assignment(identifier, expression)

    def expr(self):
        """
        Function for the expr non-terminal following the BNF rule:
        <expr> -> <term> ADD_OP <expr>
                | <term> SUB_OP <expr>
                | <term>
        """
        # enter expr
        # print("<expr>")
        # parse a term
        term = self.term()
        operator = None
        expression = None
        # check for addition or subtraction, if so parse the expression after
        if self.next_token.type == Operators.ADD_OP:
            operator = Operators.ADD_OP
            expression = self.expr()
        elif self.next_token.type == Operators.SUB_OP:
            operator = Operators.SUB_OP
            expression = self.expr()
        # exit expression
        # print("</expr>")
        return Expression(operator, term, expression)

    def term(self):
        """
        Function for the term non-terminal following the BNF rule:
        <term> -> <factor> MULT_OP <term>
                | <factor> DIV_OP <term>
                | <factor>
        """
        # enter term
        # print("<term>")
        # parse a factor
        factor = self.factor()
        operator = None
        # check for multiplication/division, if so parse another term
        self.lex()
        term = None
        if self.next_token.type == Operators.MULT_OP:
            operator = Operators.MULT_OP
            term = self.term()
        elif self.next_token.type == Operators.DIV_OP:
            operator = Operators.DIV_OP
            term = self.term()
        # exit term
        # print("</term>")
        return Term(factor, operator, term)

    def factor(self):
        """
        Function for the factor non-terminal following the BNF rule:
        <factor> -> LEFT_PEREN<expr>RIGHT_PEREN | ID | FLOAT_LIT | INT_LIT
        """
        # enter factor
        # print("<factor>")
        # look for parentheses
        self.lex()
        if self.next_token.type == Operators.LEFT_PEREN:
            type_of = type(Expression)
            # parse an expression
            value = self.expr()
            # ensure parenthesis are balanced
            if self.next_token.type != Operators.RIGHT_PEREN:
                raise ParserError(
                    self.next_token.pos, "Mismatched parenthesis")
        # if identifier. int_lit, or float_lit, reached terminal, do nothing
        elif self.next_token.type == Identifiers.IDENT:
            type_of = Identifiers.IDENT
            value = self.next_token.lexeme
        elif self.next_token.type == Literals.INT_LIT:
            type_of = Literals.INT_LIT
            value = int(self.next_token.lexeme)
        elif self.next_token.type == Literals.FLOAT_LIT:
            type_of = Literals.FLOAT_LIT
            value = float(self.next_token.lexeme)
        else:
            # raise an error if none of the above conditions matched
            raise ParserError(self.next_token.pos, "Invalid factor")
        # exit factor
        # print("</factor>")
        return Factor(type_of, value)

    def print_stmnt(self):
        """
        Function for the print_stmnt non-terminal following the BNF rule:
        <print_stmnt> -> PRINT <expr>
        """
        # enter print
        # print("<print_stmnt>")
        # parse expression
        expression = self.expr()
        # exit print
        # print("</print_stmnt>")
        return Statement.Print(expression)

    def do_while(self):
        """
        Function for the do_while non-terminal following the BNF rule:
        <do_while> -> DO WHILE <relational-expression> EOL <statement> LOOP
        """
        # enter do_while
        # print("<do_while>")
        # check for while statement
        self.lex()
        # if no while raise an error
        if self.next_token.type != Keywords.WHILE:
            raise ParserError(self.next_token.pos, "Invalid loop")
        # parse relational expression
        rel_exp = self.relational_expr()
        # parse the body
        body = self.body()
        # check for loop end else raise error
        if self.next_token.type != Keywords.LOOP:
            raise ParserError(self.next_token.pos, "Invalid loop")
        # check for loop EOL else raise error
        self.lex()
        if self.next_token.type != Delimiters.EOL:
            raise ParserError(self.next_token.pos, "Invalid loop")
        # exit do_while
        # print("</do_while>")
        return Statement.DoWhile(rel_exp, body)

    def if_stmnt(self):
        """
        Function for the if_stmnt non-terminal following the BNF rule:
        <if_stmnt> ->  IF <relational-expression> THEN EOL <body> IF EOL
        """
        # enter if_stmnt
        # print("<if_stmnt>")
        # parse relational expression
        rel_exp = self.relational_expr()
        # check for if otherwise raise error
        if self.next_token.type != Keywords.THEN:
            raise ParserError(self.next_token.pos, "Invalid if statement")
        # check for EOL, otherwise raise error
        self.lex()
        if self.next_token.type != Delimiters.EOL:
            raise ParserError(self.next_token.pos, "Invalid if statement")
        # parse the body
        body = self.body()
        # check for end if otherwise raise error
        if self.next_token.type != Keywords.IF:
            raise ParserError(self.next_token.pos, "Invalid if statement")
        # check for EOL, otherwise raise error
        self.lex()
        if self.next_token.type != Delimiters.EOL:
            raise ParserError(self.next_token.pos, "Invalid if statement")
        # exit if_stmnt
        # print("</if_stmnt>")
        return Statement.If(rel_exp, body)

    def relational_expr(self):
        """
        Function for the relational_expr non-terminal following the BNF rule:
        <relational-expression> -> <expr> EQUAL_OP <expr>
                                    | <expr> LESS_THAN <expr>
                                    | <expr> GREATER_THAN <expr>
                                    | <expr> NOT_GREATER <expr>
                                    | <expr> NOT_LESS <expr>
        """
        # enter relational_expr
        # print("<relational_expr>")
        # parse the expression
        l_expr = self.expr()
        operator = None
        # parse another expression if an operator is present
        if self.next_token.type == Operators.EQUAL_OP:
            operator = Operators.EQUAL_OP
            r_expr = self.expr()
        elif self.next_token.type == Operators.LESS_THAN:
            operator = Operators.LESS_THAN
            r_expr = self.expr()
        elif self.next_token.type == Operators.GREATER_THAN:
            operator = Operators.GREATER_THAN
            r_expr = self.expr()
        elif self.next_token.type == Operators.NOT_GREATER:
            operator = Operators.NOT_GREATER
            r_expr = self.expr()
        elif self.next_token.type == Operators.NOT_LESS:
            operator = Operators.NOT_LESS
            r_expr = self.expr()
        # exit relational_expr
        # print("</relational_expr>")
        return RelationalExpression(l_expr, operator, r_expr)

    def body(self):
        """
        Function for the body non-terminal following the BNF rule:
        body -> <statement><body>
            |<statement> IF
            |<statement> LOOP
        """
        # enter body
        # print("<body>")
        statements = []
        self.lex()
        # parse statements while not end of loop/if statement
        while(self.next_token.type != Keywords.IF
              and self.next_token.type != Keywords.LOOP):
            statements.append(self.statement())
            self.lex()
        # exit body
        # print("</body>")
        return statements

    def lex(self):
        """
        retrieves next token from scanner and assigns the next token to a
        instance available variable, to be used by other parser functions.
        """
        try:
            # get the next token
            token = next(self.lexer)
        except ScannerError as e:
            # catch any errors and print them
            print(e)
        # print the token
        # print(token)
        self.next_token = token


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
        # try catch to catch any parser errors
        try:
            # start parsing the program
            parse_tree = parser.program()
        except ParserError as e:
            # if a parsing error occurred, alert the user
            print(e)
        except Exception as e:
            # print any other errors
            print(e)


if __name__ == "__main__":
    main()
