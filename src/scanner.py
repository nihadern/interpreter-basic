"""
Python Implementation of a Scanner for a Subset of BASIC (ECMA 116 Standard)
Created by Nihad Kalathingal on 2/23/2020. Modified (03-04-2020)
    Kennesaw State University
    College of Computing and Software Engineering
    Department of Computer Science
    4308 Concepts of Programming Languages 03
    Module 3 – 1st Deliverable
    Nihad Kalathingal (nkalathi@students.kennesaw.edu)
"""

import re  # import regex library used to match lexemes
import sys  # import sys library used for CLI arguments
from basic_subset import *   # import the basic subset to be used

"""
The scanner is implemented in the Scanner class which uses the rules
specified in the basic_subset.py file. The scanner is instansiated
with a source file and returns the associated tokens in that file.
The scanner throws an exception of type ScannerError if a unkown lexeme
is found. The class Token is the output of the Scanner which contains
the type, postion, and lexeme which is to be used by other parts of the
interpreter.
"""


class Token:
    """
    Class for token which contains the type, postion, and lexeme.
    """
    def __init__(self, type: Tokens, lexeme: str, pos: tuple):
        """
        Simple constructor to assign token attributes

        Parameters:
        type (Tokens): the token encoded as an enum
        lexeme (str): the lexeme that was matched
        pos (tuple): tuple of length 2 of the form (row, column)
        """
        self.type = type
        self.lexeme = lexeme
        self.pos = pos

    def __str__(self):
        """
        Returns the human readable string defenition of a token
        """
        str_form = ("Ln:{:<3} Col:{:<4} Token: {:<30}"
                    "Lexeme: {:<20}")
        return str_form.format(self.pos[0], self.pos[1], self.type,
                               repr(self.lexeme))


class ScannerError(Exception):
    """
    Exception class for a scanner error.
    Used in case a lexeme is not found.
    """
    def __init__(self, pos: tuple):
        """
        Simple constructor to assign ScannerError attributes.

        Parameters:
        pos (tuple): tuple of length 2 of the form (row, column)
        """
        self.pos = pos  # position of error

    def __str__(self):
        """
        Returns an error message with details of the error.
        """
        return "ERORR: Unknown lexeme at Ln:{} Col:{}".format(self.pos[0],
                                                              self.pos[1])


class Scanner:
    """
    Scanner class which tokenizes from a given buffer based on regex rules
    for lexemes.
    """
    def __init__(self, source):
        """
        Simple constructor to assign Scanner attributes.

        Parameters:
        source (Buffer): source file/buffer
        """
        self.source = source  # source code

    def __match_token(self, group):
        """
        Internaly used function that matches a token in a specified group.

        Parameters:
        source (tuple): tuple of tuples which contain the compiled rule
                        and Enum for tokens for which to perform match to.
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
        Generates a Token object for each lexeme found per regex rules.
        """
        # iterate through lines in the buffer
        for self.line_num, self.line in enumerate(self.source):
            self.pos = 0  # position of the lexeme in line
            while self.pos < len(self.line):  # iterate while not end of line
                # skip whitespace
                ws = WS_RULE.search(self.line, self.pos)
                if ws:
                    self.pos = ws.start()
                # if first char is alpha look in alpha group
                if self.line[self.pos].isalpha():
                    yield self.__match_token(ALPHA)
                # if not look in unknown group
                else:
                    yield self.__match_token(NON_ALPHA)
        # generate the EOF token for the EOF
        yield Token(Delimiters.EOF, "/Z", (self.line_num+1, self.pos+1))


# ------------------------ main --------------------------------------------
if __name__ == "__main__":
    '''
    Ensure that the Python 3 interpreter is installed.
    The scanner can be used with BASIC file using the following command:

    python3 scanner.py <filename>

    For example:
    python3 scanner.py test.bas

    Ensure that the file is in the same folder as the script or provide an
    a path to file.
    '''
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
