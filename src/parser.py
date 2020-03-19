from scanner import *
from basic_subset import *
import sys


class ParserError(Exception):
    """
    Exception class for a Parser error.
    Used in case a parsing error occurs.
    """
    def __init__(self, pos: tuple, err=None):
        """
        Simple constructor to assign ScannerError attributes.

        Parameters:
        pos (tuple): tuple of length 2 of the form (row, column)
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
        return "ERORR: {} Ln:{} Col:{}".format(self.err, self.pos[0],
                                               self.pos[1])


# <program> -> <statements>
def program():
    print("<program>")
    statements()
    print("</program>")


# <statements> -> <statement>
# 		| <statement> EOL <statements> END
def statements():
    print("<statements>")
    statement()
    lex()
    if next_token.type == Delimiters.EOL:
        statements()
    elif next_token.type == Keywords.END:
        print("</statements>")
    else:
        raise ParserError(next_token.pos, "Invalid statements")


# <statement> -> <assn_stmnt>
# 		| <print_stmnt>
# 		| <do_while>
# 		| <if_stmnt>
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
    if next_token.type != Identifiers.IDENT:
        raise ParserError(next_token.pos, "Invalid assignment statement")
    print("</assn_stmnt>")


# <expr> -> <expr> ADD_OP <term> | <expr> SUB_OP <term>
def expr():
    print("<expr>")
    lex()
    if next_token != Operators.ADD_OP or next_token != Operators.SUB_OP:
        expr()
    else:
        term()
    term()
    print("</expr>")


# <term> -> <term> MULT_OP <factor>
# 	| <term> DIV_OP <factor>
# 	| <factor>
def term():
    print("<term>")
    lex()
    if next_token == Operators.MULT_OP or next_token == Operators.DIV_OP:
        factor()
    else:
        factor()
    # TODO: how to fix the factor alone issue
    print("</term>")


# <factor> -> LEFT_PEREN<expr>RIGHT_PEREN | ID | FLOAT_LIT | INT_LIT
def factor():
    print("<factor>")
    lex()
    if next_token == Operators.LEFT_PEREN:
        expr()
        lex()
        if next_token != Operators.RIGHT_PEREN:
            raise ParserError("Mismatched perenthesis", next_token.pos)
    elif next_token == Identifiers.IDENT:
        pass
    elif next_token == Literals.INT_LIT:
        pass
    elif next_token == Literals.FLOAT_LIT:
        pass
    else:
        raise ParserError("Invalid factor", next_token.pos)

    print("</factor>")


# <print_stmnt> -> PRINT <expr>
def print_stmnt():
    print("<print_stmnt>")
    expr()
    print("</print_stmnt>")


# <do_while> -> DO WHILE <relational-expression> EOL <body>
def do_while():
    print("<do_while>")
    lex()
    if next_token.type != Keywords.WHILE:
        raise ParserError("Invalid loop", next_token.pos)
    relational_expr()
    lex()
    if next_token.type != Delimiters.EOL:
        raise ParserError("Invalid loop", next_token.pos)
    body()
    lex()
    if next_token.type != Delimiters.EOL:
        raise ParserError("Invalid loop", next_token.pos)
    print("</do_while>")


# <if_stmnt> ->  IF <relational-expression> THEN EOL <body> IF
def if_stmnt():
    print("<if_stmnt>")
    relational_expr()
    lex()
    if next_token.type != Keywords.THEN:
        raise ParserError("Invalid if statement", next_token.pos)
    lex()
    if next_token.type != Delimiters.EOL:
        raise ParserError("Invalid if statement", next_token.pos)
    body()
    if next_token.type != Keywords.IF:
        raise ParserError("Invalid if statement", next_token.pos)
    print("</if_stmnt>")


# <body> -> <statement> LOOP
# 	| <statement> EOL <body> EOL LOOP
#   | <statement> EOL <body> EOL END
def body():
    print("<body>")
    statement()
    lex()
    if next_token.type != Delimiters.EOL:
        raise ParserError("Invalid body", next_token.pos)
    if next_token.type != Keywords.LOOP or next_token.type != Keywords.END:
        body()
    print("</body>")


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
    token = next(scanner.lex())
    print(token.lexeme)
    global next_token
    next_token = token


if __name__ == "__main__":
    filename = sys.argv[1]
    # use with function to open/close file and use exception handling
    with open(filename, "r") as f:
        scanner = Scanner(f)  # create a scanner object with a source file
        # try catch to catch any scanner errors
        try:
            program()
        except ParserError as e:
            print(e)
