"""
A Subset of BASIC (ECMA 116 Standard)
Created by Nihad Kalathingal on 2/23/2020. Modified (03-01-2020)
    Kennesaw State University
    College of Computing and Software Engineering
    Department of Computer Science
    4308 Concepts of Programming Languages 03
    Module 3 – 1st Deliverable
    Nihad Kalathingal (nkalathi@students.kennesaw.edu)
"""

from enum import Enum, auto  # enumerator for lexemes
import re  # import regex library used to define lexemes

"""
    This file includes the definitions for the basic subset chosen from the
    ECMA 116 Standard. The Tokens are described as Enums which inherit from
    a base class into children with Token types. A ALPHA and NON_ALPHA tuple
    defines the lexemes using regular expressions as well as the order in 
    which they are matched in the scanner.
"""


class Tokens(Enum):
    """
    Base class of tokens of the BASIC subset encoded as an enumeration.
    """
    pass


class Delimiters(Tokens):
    """Delimiters in the basic subset."""
    EOL = auto()
    EOF = auto()


class Identifiers(Tokens):
    """Identifiers in the basic subset."""
    IDENT = auto()


class Keywords(Tokens):
    """Keywords in the basic subset."""
    PRINT = auto()
    IF = auto()
    THEN = auto()
    LET = auto()
    END = auto()
    DO = auto()
    WHILE = auto()
    LOOP = auto()


class Literals(Tokens):
    """Literals in the basic subset."""
    INT_LIT = auto()
    FLOAT_LIT = auto()


class Operators(Tokens):
    """Operators in the basic subset."""
    ADD_OP = auto()
    SUB_OP = auto()
    EQUAL_OP = auto()
    LESS_THAN = auto()
    GREATER_THAN = auto()
    NOT_GREATER = auto()
    NOT_LESS = auto()
    RIGHT_PEREN = auto()
    LEFT_PEREN = auto()


# regex matching order for tokens that start with alpha char
# i.e keywords/ identifier
ALPHA = (
    # check for keywords
    (re.compile(r'IF', re.IGNORECASE), Keywords.IF),
    (re.compile(r'THEN', re.IGNORECASE), Keywords.THEN),
    (re.compile(r'PRINT', re.IGNORECASE), Keywords.PRINT),
    (re.compile(r'LET', re.IGNORECASE), Keywords.LET),
    (re.compile(r'END', re.IGNORECASE), Keywords.END),
    (re.compile(r'DO', re.IGNORECASE), Keywords.DO),
    (re.compile(r'WHILE', re.IGNORECASE), Keywords.WHILE),
    (re.compile(r'LOOP', re.IGNORECASE), Keywords.LOOP),
    # check for identifier last
    (re.compile(r'[A-Za-z0-9_]{1,31}'), Identifiers.IDENT)
)
# regex matching order for tokens that start with non-alpha starting char
# i.e. data types, operators, identifier
NON_ALPHA = (
    # check for the two data types, float and integer
    (re.compile(r'[-+]?\d*\.\d+'), Literals.FLOAT_LIT),
    (re.compile(r'[-+]?[0-9]+'), Literals.INT_LIT),
    # check for operators
    (re.compile(r'\)'), Operators.RIGHT_PEREN),
    (re.compile(r'\('), Operators.LEFT_PEREN),
    (re.compile(r'\+'), Operators.ADD_OP),
    (re.compile(r'\-'), Operators.SUB_OP),
    (re.compile(r'='), Operators.EQUAL_OP),
    (re.compile(r'<'), Operators.LESS_THAN),
    (re.compile(r'>'), Operators.GREATER_THAN),
    (re.compile(r'<='), Operators.NOT_GREATER),
    (re.compile(r'>='), Operators.NOT_LESS),
    # check for end of line
    (re.compile(r'\n'), Delimiters.EOL),
    # check for identifier last
    (re.compile(r'[A-Za-z0-9_]{1,31}'), Identifiers.IDENT)
)
# regex rule used to skip whitespaces
WS_RULE = re.compile(r"\S|\r\n|\r|\n")
