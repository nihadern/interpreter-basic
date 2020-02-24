"""
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


class Tokens(Enum):
    """
    Tokens of the basic subset encoded as an enumeration
    """
    PRINT_STMNT = auto()
    INT_LIT = auto()
    EOL = auto()
    ADD_OP = auto()
    SUB_OP = auto()
    ASSN_OP = auto()
    LESS_THAN = auto()
    GREATER_THAN = auto()
    IF_STMNT = auto()
    THEN_STMNT = auto()
    IDENT = auto()
    EOF = auto()


class Token:
    """
    Class for token which holds the type, postion, and lexeme
    """
    def __init__(self, type: Tokens, lexeme: str, pos: tuple):
        """
        Simple constructor to assign object attributes
        """
        self.type = type
        self.lexeme = lexeme
        self.pos = pos

    def __str__(self):
        """
        Returns the string defenition of a token
        """
        str_form = "Token: {}, Lexeme: {}, Position: {}:{}"
        return str_form.format(self.type.name, self.lexeme,
                               self.pos[0], self.pos[1])


class Scanner:
    """
    Scanner class which lexes from a buffer
    """
    def __init__(self, source, rules: list):
        self.source = source  # source code
        # regex rules
        self.rules = []
        for pattern, token in rules:
            regex = re.compile(pattern, re.IGNORECASE)
            self.rules.append((regex, token))
        self.ws_rule = re.compile(r"\S")

    def lex(self, skip_ws=True):
        """
        Generates a Token object for each lexeme found per regex rules
        """
        # iterate through lines in the buffer
        for line_num, line in enumerate(self.source):
            line = line.strip()  # remove spaces/ trim
            pos = 0  # position of the lexeme in line
            while pos < len(line):  # iterate while not end of line
                # skip whitespace
                if skip_ws:
                    ws = self.ws_rule.search(line, pos)
                    if ws:
                        pos = ws.start()
                match = None  # set to no matches found for lexeme
                # Iterate trhough available rules for lexemes
                for regex, token_type in self.rules:
                    match = regex.match(line, pos)  # check for a match
                    if match:
                        # create a token for the match
                        token = Token(token_type, match.group(0),
                                      (line_num, pos))
                        # set position to end of last token
                        pos = match.end()
                        # generate token
                        yield token
                        break
                # if there is no match raise an error
                if not match:
                    raise ScannerError((line_num, pos))
        # generate the EOF token for the EOF
        yield Token(Tokens.EOF, "/Z", (line_num, pos))


# Questions:
# lexeme size limit?
# Identifiers processed seperately?
# Do integers need to be assigned to tokens?
# what is max identifier length?
# is EOL a token?
# have object store state and not yield?
# syntax representation- do we need grmmar or is regex sufficient?
# redisign for isdigit, isletter etc?
# do i need to support line numbers if no goto statement exists
# CITE SOURCES

if __name__ == "__main__":
    RULES = [
        (r'PRINT', Tokens.PRINT_STMNT),
        (r'[-+]?[0-9]+', Tokens.INT_LIT),
        (r'\n', Tokens.EOL),
        (r'\+', Tokens.ADD_OP),
        (r'\-', Tokens.SUB_OP),
        (r'=', Tokens.ASSN_OP),
        (r'<', Tokens.LESS_THAN),
        (r'>', Tokens.GREATER_THAN),
        (r'IF', Tokens.IF_STMNT),
        (r'THEN', Tokens.THEN_STMNT),
        (r'[A-Za-z_][A-Za-z0-9_]*', Tokens.IDENT),
    ]
    filename = sys.argv[1]
    with open(filename, "r") as f:
        scanner = Scanner(f, RULES)
        try:
            for token in scanner.lex():
                print(token)
        except ScannerError as e:
            print("ERORR: Unknown lexeme at {}:{}".format(e.pos[0], e.pos[1]))
