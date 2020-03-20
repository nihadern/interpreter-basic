"""
Python Implementation of a Parser for a Subset of BASIC (ECMA 116 Standard)
Created by Nihad Kalathingal and Nick Green on 3/19/2020. Modified (03-20-2020)
    Kennesaw State University
    College of Computing and Software Engineering
    Department of Computer Science
    4308 Concepts of Programming Languages 03
    Module 3 – 2nd Deliverable
    Nihad Kalathingal (nkalathi@students.kennesaw.edu)
"""

from scanner import *   # import scanner and scanner errors
from basic_subset import *  # import the basic subset with the tokens
import sys  # import sys used for CLI args


# global varibales used through parser functions
global lexer  # the generator of lexemes from the scanner
global next_token  # next token / look ahead from scanner
next_token = None
lexer = None


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


def program():
    """
    Starting point for the parser.
    Function for the program non-terminal following the BNF rule:
    <program> -> <statements>
    """
    # enter program
    print("<program>")
    # parse statements
    statements()
    # exit program
    print("</program>")


def statements():
    """
    Function for the statements non-terminal following the BNF rule:
    <statements> -> <statement>
                    | <statement> EOL <statements>
    """
    # parse statemnt
    lex()
    statement()
    # while mext token EOL parse statements
    if next_token.type == Delimiters.EOL:
        statements()


def statement():
    """
    Function for the statement non-terminal following the BNF rule:
    <statement> -> <assn_stmnt>
                | <print_stmnt>
                | <do_while>
                | <if_stmnt>
                | END
    """
    # enter statement
    print("<statement>")
    # choose type of statement based on next_token
    if next_token.type == Keywords.LET:
        assn_stmnt()
    elif next_token.type == Keywords.PRINT:
        print_stmnt()
    elif next_token.type == Keywords.DO:
        do_while()
    elif next_token.type == Keywords.IF:
        if_stmnt()
    elif next_token.type == Keywords.END:
        # end of program/statement, do nothing
        pass
    elif next_token.type == Delimiters.EOL:
        #  empty statement/line, do nothing
        pass
    else:
        # raise a parsing error as its not a valid statement
        raise ParserError(next_token.pos, "Invalid type of statement")
    # exit statement
    print("</statement>")


def assn_stmnt():
    """
    Function for the assn_stmnt non-terminal following the BNF rule:
    <assn_stment> -> LET IDENT EQUAL_OP <expr>
    """
    # enter assig_stmnt
    print("<assn_stmnt>")
    # check for identifier
    lex()
    if next_token.type != Identifiers.IDENT:
        raise ParserError(next_token.pos,
                          "Invalid identifier in assignment statement")
    # check for assinment operator
    lex()
    if next_token.type != Operators.EQUAL_OP:
        raise ParserError(next_token.pos, "Invalid assignment statement")
    # parse an expression
    expr()
    # exit assig_stmnt
    print("</assn_stmnt>")


def expr():
    """
    Function for the expr non-terminal following the BNF rule:
    <expr> -> <term> ADD_OP <expr>
            | <term> SUB_OP <expr>
            | <term>
    """
    # enter expr
    print("<expr>")
    # parse a term
    term()
    # check for addition or subtraction, if so parse the expression after
    if next_token.type == Operators.ADD_OP:
        expr()
    elif next_token.type == Operators.SUB_OP:
        expr()
    # exit expression
    print("</expr>")


def term():
    """
    Function for the term non-terminal following the BNF rule:
    <term> -> <factor> MULT_OP <term>
            | <factor> DIV_OP <term>
            | <factor>
    """
    # enter term
    print("<term>")
    # parse a factor
    factor()
    # check for multiplication/division, if so parse another term
    lex()
    if next_token.type == Operators.MULT_OP:
        term()
    elif next_token.type == Operators.DIV_OP:
        term()
    # exit term
    print("</term>")


def factor():
    """
    Function for the factor non-terminal following the BNF rule:
    <factor> -> LEFT_PEREN<expr>RIGHT_PEREN | ID | FLOAT_LIT | INT_LIT
    """
    # enter factor
    print("<factor>")
    # look for perenthises
    lex()
    if next_token.type == Operators.LEFT_PEREN:
        # parse an expression
        expr()
        # ensure perenthesis are balanced
        if next_token.type != Operators.RIGHT_PEREN:
            raise ParserError(next_token.pos, "Mismatched perenthesis")
    # if identifier. int_lit, or float_lit, reached terminal, do nothing
    elif next_token.type == Identifiers.IDENT:
        pass
    elif next_token.type == Literals.INT_LIT:
        pass
    elif next_token.type == Literals.FLOAT_LIT:
        pass
    else:
        # raise an error if none of the above conditions matched
        raise ParserError(next_token.pos, "Invalid factor")
    # exit factor
    print("</factor>")


def print_stmnt():
    """
    Function for the print_stmnt non-terminal following the BNF rule:
    <print_stmnt> -> PRINT <expr>
    """
    # enter print
    print("<print_stmnt>")
    # parse expression
    expr()
    # exit print
    print("</print_stmnt>")


def do_while():
    """
    Function for the do_while non-terminal following the BNF rule:
    <do_while> -> DO WHILE <relational-expression> EOL <statement> LOOP
    """
    # enter do_while
    print("<do_while>")
    # check for while statement
    lex()
    # if no while raise an error
    if next_token.type != Keywords.WHILE:
        raise ParserError(next_token.pos, "Invalid loop")
    # parse relational expression
    relational_expr()
    # parse the body
    body()
    # check for loop end else raise error
    if next_token.type != Keywords.LOOP:
        raise ParserError(next_token.pos, "Invalid loop")
    # check for loop EOL else raise error
    lex()
    if next_token.type != Delimiters.EOL:
        raise ParserError(next_token.pos, "Invalid loop")
    # exit do_while
    print("</do_while>")


def if_stmnt():
    """
    Function for the if_stmnt non-terminal following the BNF rule:
    <if_stmnt> ->  IF <relational-expression> THEN EOL <body> IF EOL
    """
    # enter if_stmnt
    print("<if_stmnt>")
    # parse relational expression
    relational_expr()
    # check for if otherwise raise error
    if next_token.type != Keywords.THEN:
        raise ParserError(next_token.pos, "Invalid if statement")
    # check for EOL, otherwise raise error
    lex()
    if next_token.type != Delimiters.EOL:
        raise ParserError(next_token.pos, "Invalid if statement")
    # parse the body
    body()
    # check for end if otherwise raise error
    if next_token.type != Keywords.IF:
        raise ParserError(next_token.pos, "Invalid if statement")
    # check for EOL, otherwise raise error
    lex()
    if next_token.type != Delimiters.EOL:
        raise ParserError(next_token.pos, "Invalid if statement")
    # exit if_stmnt
    print("</if_stmnt>")


def relational_expr():
    """
    Function for the relational_expr non-terminal following the BNF rule:
    <relational-expression> -> <expr> EQUAL_OP <expr>
                                | <expr> LESS_THAN <expr>
                                | <expr> GREATER_THAN <expr>
                                | <expr> NOT_GREATER <expr>
                                | <expr> NOT_LESS <expr>
    """
    # enter relational_expr
    print("<relational_expr>")
    # parse the expression
    expr()
    # parse another expression if an operator is present
    if next_token.type == Operators.EQUAL_OP:
        expr()
    elif next_token.type == Operators.LESS_THAN:
        expr()
    elif next_token.type == Operators.GREATER_THAN:
        expr()
    elif next_token.type == Operators.NOT_GREATER:
        expr()
    elif next_token.type == Operators.NOT_LESS:
        expr()
    # exit relational_expr
    print("</relational_expr>")


def body():
    """
    Function for the body non-terminal following the BNF rule:
    body -> <statement><body>
        |<statement> IF
        |<statement> LOOP
    """
    # enter body
    print("<body>")
    lex()
    # parse statements while not end of loop/if statement
    while(next_token.type != Keywords.IF and next_token.type != Keywords.LOOP):
        statement()
        lex()
    # exit body
    print("</body>")


def lex():
    """
    retrieves next token from scanner and assings the next token to a globally
    avilable varibale, to be used by other parser functions.
    """
    try:
        # get the next token
        token = next(lexer)
    except ScannerError as e:
        # catch any errors and print them
        print(e)
    # print the token
    print(token)
    # make next token global and available to other fuctions
    global next_token
    next_token = token


if __name__ == "__main__":
    filename = sys.argv[1]
    # use with function to open/close file and use exception handling
    with open(filename, "r") as f:
        scanner = Scanner(f)  # create a scanner object with a source file
        # make the generator global to be used with parser functions
        lexer = scanner.lex()
        # try catch to catch any parser errors
        try:
            # start parsing the program
            program()
        except ParserError as e:
            # if a parsing error occured, alert the user
            print(e)
        except Exception as e:
            # print any other errors
            print(e)
