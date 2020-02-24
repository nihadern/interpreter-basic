"""
Python Implementation of a Scanner for a Subset of BASIC (ECMA 116 Standard)
Created by Nihad Kalathingal on 2/23/2020. Modified (05-01-19)
    Kennesaw State University
    College of Computing and Software Engineering
    Department of Computer Science
    4308 Concepts of Programming Languages 03
    Module 3 – 1st Deliverable
    Nihad Kalathingal (nkalathi@students.kennesaw.edu)
"""

import re  # import regex library used to define lexemes
import sys  # import sys library used for CLI arguments
from enum import Enum, auto  # enumerator for lexemes


class ScannerError(Exception):
    """
    Exception class for a scanner error.
    Used in case a lexeme is not found
    """
    def __init__(self, pos: tuple):
        self.pos = pos  # position of tuple

    def __str__(self):
        """
        Returns an error message with details of the error
        """
        return "ERORR: Unknown lexeme at {}:{}".format(self.pos[0],
                                                       self.pos[1])


class Tokens(Enum):
    """
    Tokens of the BASIC subset encoded as an enumeration
    """
    PRINT_STMNT = auto()
    INT_LIT = auto()
    FLOAT_LIT = auto()
    EOL = auto()
    ADD_OP = auto()
    SUB_OP = auto()
    EQUAL_OP = auto()
    LESS_THAN = auto()
    GREATER_THAN = auto()
    NOT_GREATER = auto()
    NOT_LESS = auto()
    IF_STMNT = auto()
    THEN_STMNT = auto()
    IDENT = auto()
    EOF = auto()
    LET = auto()


class Token:
    """
    Class for token which contains the type, postion, and lexeme
    """
    def __init__(self, type: Tokens, lexeme: str, pos: tuple):
        """
        Simple constructor to assign token attributes
        """
        self.type = type
        self.lexeme = lexeme
        self.pos = pos

    def __str__(self):
        """
        Returns the human readable string defenition of a token
        """
        str_form = "{}:{} - Token: {}, Lexeme: {}"
        return repr(str_form.format(self.pos[0], self.pos[1],
                                    self.type.name, self.lexeme))


class Scanner:
    """
    Scanner class which tokenizes from a given buffer based on regex rules
    for lexemes
    """
    # regex matching order for tokens that start with alpha char
    # i.e keywords/ identifier
    ALPHA = [
        # check for keywords
        (re.compile(r'IF', re.IGNORECASE), Tokens.IF_STMNT),
        (re.compile(r'THEN', re.IGNORECASE), Tokens.THEN_STMNT),
        (re.compile(r'PRINT', re.IGNORECASE), Tokens.PRINT_STMNT),
        (re.compile(r'LET', re.IGNORECASE), Tokens.LET),
        # check for identifier last
        (re.compile(r'[A-Za-z0-9_]{1,31}'), Tokens.IDENT)
    ]
    # regex matching order for tokens that start with non-alpha starting char
    # i.e. data types, operators, identifier
    UKNOWN = [
        # check for the two data types, float and integer
        (re.compile(r'[-+]?\d*\.\d+'), Tokens.FLOAT_LIT),
        (re.compile(r'[-+]?[0-9]+'), Tokens.INT_LIT),
        # check for operators
        (re.compile(r'\n'), Tokens.EOL),
        (re.compile(r'\+'), Tokens.ADD_OP),
        (re.compile(r'\-'), Tokens.SUB_OP),
        (re.compile(r'='), Tokens.EQUAL_OP),
        (re.compile(r'<'), Tokens.LESS_THAN),
        (re.compile(r'>'), Tokens.GREATER_THAN),
        (re.compile(r'<='), Tokens.NOT_GREATER),
        (re.compile(r'>='), Tokens.NOT_LESS),
        # check for identifier last
        (re.compile(r'[A-Za-z0-9_]{1,31}'), Tokens.IDENT)
    ]
    # regex rule used to skip whitespaces
    WS_RULE = re.compile(r"\S|\r\n|\r|\n")

    def __init__(self, source):
        self.source = source  # source code

    def _match_token(self, group):
        """
        Internaly used function that matches a token in a specified group
        """
        match = None  # set to no matches found for lexeme
        # Iterate trhough available rules for lexemes
        for regex, token_type in group:
            match = regex.match(self.line, self.pos)  # check for a match
            if match:
                # create a token for the match
                token = Token(token_type, match.group(0),
                              (self.line_num+1, self.pos+1))
                # set position to end of last token
                self.pos = match.end()
                # generate token
                return token
        # if there is no match raise an error
        if not match:
            raise ScannerError((self.line_num+1, self.pos+1))

    def lex(self):
        """
        Generates a Token object for each lexeme found per regex rules
        """
        # iterate through lines in the buffer
        for self.line_num, self.line in enumerate(self.source):
            self.pos = 0  # position of the lexeme in line
            while self.pos < len(self.line):  # iterate while not end of line
                # skip whitespace
                ws = self.WS_RULE.search(self.line, self.pos)
                if ws:
                    self.pos = ws.start()
                # if first char is alpha look in alpha group
                if self.line[self.pos].isalpha():
                    yield self._match_token(self.ALPHA)
                # if not look in unknown group
                else:
                    yield self._match_token(self.UKNOWN)
        # generate the EOF token for the EOF
        yield Token(Tokens.EOF, "/Z", (self.line_num+1, self.pos+1))


# ------------------------ main --------------------------------------------
if __name__ == "__main__":
    # get the filename from the first CLI argument
    filename = sys.argv[1]
    # use with function to open/close file and use exception handling
    with open(filename, "r") as f:
        scanner = Scanner(f)  # create a scanner object with a source file
        # try catch to catch any scanner errors
        try:
            # iterate through tokens and print
            for token in scanner.lex():
                print(token)
        except ScannerError as e:
            # print an error if uknown lexeme is found
            print(e)
