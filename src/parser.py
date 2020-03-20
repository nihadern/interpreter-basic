from scanner import *
from basic_subset import *
import sys


# global varibales used through parser functions
global lexer
global next_token
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


# <program> -> <statements>
def program():
    print("<program>")
    statements()
    print("</program>")


# <statements> -> <statement>
# 		| <statement> EOL <statements>
def statements():
    # print("<statements>")
    statement()
    if next_token.type == Delimiters.EOL:
        statements()
    # else:
    #     raise ParserError(next_token.pos, "Invalid statements")


# <statement> -> <assn_stmnt>
# 		| <print_stmnt>
# 		| <do_while>
# 		| <if_stmnt>
#       | END
def statement():
    print("<statement>")
    lex()
    if next_token.type == Keywords.LET:
        assn_stmnt()
    elif next_token.type == Keywords.PRINT:
        print_stmnt()
    elif next_token.type == Keywords.DO:
        do_while()
    elif next_token.type == Keywords.IF:
        if_stmnt()
    elif next_token.type == Keywords.END:
        # end of programs, do nothing
        pass
    elif next_token.type == Delimiters.EOL:
        #  empty statement/line, do nothing
        pass
    else:
        raise ParserError(next_token.pos, "Invalid type of statement")

    print("</statement>")


# # <assn_stment> -> LET IDENT EQUAL_OP <expr>
def assn_stmnt():
    print("<assn_stmnt>")
    lex()
    if next_token.type != Identifiers.IDENT:
        raise ParserError(next_token.pos,
                          "Invalid identifier in assignment statement")
    lex()
    if next_token.type != Operators.EQUAL_OP:
        raise ParserError(next_token.pos, "Invalid assignment statement")
    expr()
    print("</assn_stmnt>")


# <expr> -> <term> ADD_OP <expr>
#           | <term> SUB_OP <expr>
#           | <term>
def expr():
    print("<expr>")
    term()
    if next_token.type == Operators.ADD_OP:
        expr()
    elif next_token.type == Operators.SUB_OP:
        expr()  
    print("</expr>")


# <term> -> <factor> MULT_OP <term>
# 	| <factor> DIV_OP <term>
# 	| <factor>
def term():
    print("<term>")
    factor()
    lex()
    if next_token.type == Operators.MULT_OP:
        term()
    elif next_token.type == Operators.DIV_OP:
        term()
    print("</term>")


# <factor> -> LEFT_PEREN<expr>RIGHT_PEREN | ID | FLOAT_LIT | INT_LIT
def factor():
    print("<factor>")
    lex()

    if next_token.type == Operators.LEFT_PEREN:
        expr()
        if next_token.type != Operators.RIGHT_PEREN:
            raise ParserError(next_token.pos, "Mismatched perenthesis")
    elif next_token.type == Identifiers.IDENT:
        pass
    elif next_token.type == Literals.INT_LIT:
        pass
    elif next_token.type == Literals.FLOAT_LIT:
        pass
    else:
        raise ParserError(next_token.pos, "Invalid factor")

    print("</factor>")


# <print_stmnt> -> PRINT <expr>
def print_stmnt():
    print("<print_stmnt>")
    expr()
    print("</print_stmnt>")


# <do_while> -> DO WHILE <relational-expression> EOL <statement> LOOP
def do_while():
    print("<do_while>")
    lex()
    if next_token.type != Keywords.WHILE:
        raise ParserError(next_token.pos, "Invalid loop")
    relational_expr()
    statement()
    lex()
    if next_token.type != Keywords.LOOP:
        raise ParserError(next_token.pos, "Invalid loop")
    lex()
    if next_token.type != Delimiters.EOL:
        raise ParserError(next_token.pos, "Invalid loop")
    print("</do_while>")


# <if_stmnt> ->  IF <relational-expression> THEN EOL <statement> END IF
def if_stmnt():
    print("<if_stmnt>")
    relational_expr()
    # lex()
    if next_token.type != Keywords.THEN:
        raise ParserError(next_token.pos, "Invalid if statement")
    lex()
    if next_token.type != Delimiters.EOL:
        raise ParserError(next_token.pos, "Invalid if statement")
    statement()
    lex()
    if next_token.type != Keywords.END:
        raise ParserError(next_token.pos, "Invalid loop")
    lex()
    if next_token.type != Keywords.IF:
        raise ParserError(next_token.pos, "Invalid loop")
    lex()
    if next_token.type != Delimiters.EOL:
        raise ParserError(next_token.pos, "Invalid loop")
    print("</if_stmnt>")


# <relational-expression> -> <expr> EQUAL_OP <expr>
# 			| <expr> LESS_THAN <expr>
# 			| <expr> GREATER_THAN <expr>
# 			| <expr> NOT_GREATER <expr>
# 			| <expr> NOT_LESS <expr>
def relational_expr():
    print("<relational_expr>")
    expr()
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
    print("</relational_expr>")


def lex():
    try:
        # get the next token
        token = next(lexer)
    except ScannerError as e:
        # catch any errors and print them
        print(e)
    # prin the token
    print(token)
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
            program()
        except ParserError as e:
            print(e.with_traceback())
