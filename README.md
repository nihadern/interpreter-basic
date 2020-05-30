# interpreter-basic
An interpreter for a subset of the BASIC language written in Python.
# Summary 
The subset of BASIC chosen includes integers, floats, print statement, if -then statements, do-while loop, assignment statement, and basic float/integer operations. The subset grammar is specified on this report with BNF and the lexemes are specified with regular expressions. Overall, this subset provides a few data types with some control flow statements and standard output (of the available data types).
BASIC Subset Syntax Specification
The subset chosen is based on the ECMA-116 standard for BASIC. Some basic features like line numbers are omitted for simplicity (line numbers are unnecessary as the GOTO statement is not implemented in this subset). The grammar for the subset can be defined as follows in BNF:
```

<program> -> <statements>
<statements> -> <statement>
                    | <statement> EOL <statements>
<statement> -> <assn_stmnt>
                | <print_stmnt>
                | <do_while>
                | <if_stmnt>
                | END
<assn_stment> -> LET IDENT EQUAL_OP <expr>
<expression> -> <addition> ((EQUAL_OP | LESS_THAN |  GREATER_THAN | NOT_GREATER | NOT_LESS) <addition>)*
<addition> -> <multiplication> <addition> ((ADD_OP | SUB_OP) <multiplication>)*
<multiplication> -> <unary> ((DIV_OP | MULT_OP) <unary>)*
<unary> -> (ADD_OP | SUB_OP) <unary> | <primary>
<primary> -> FLOAT_LIT | INT_LIT | INT_LIT | RIGHT_PEREN <expr>  LEFT_PEREN
<print_stmnt> -> PRINT <expr>
<do_while> -> DO WHILE <relational-expression> EOL <body> LOOP EOL
<if_stmnt> ->  IF <relational-expression> THEN EOL <body> IF EOL
body -> <statement><body>
        |<statement> IF
        |<statement> LOOP

```
The bracketed expressions are non-terminals and capital expressions are terminals in the above grammar. The lexemes corresponding to the above grammar can be defined with regular expressions: 
# Token	Regular Expression 
```
Keywords
PRINT		/PRINT/i
IF		/IF/i
THEN		/THEN/i
LET		/LET/i
END		/END/i
DO		/DO/i
WHILE		/WHILE/i
LOOP		/LOOP/i
Literals
FLOAT_LIT	/\d*\.\d+ /
INT_LIT		/[0-9]+/
Operators
RIGHT_PEREN	/\)/
LEFT_PEREN	/\(/
ADD_OP		/\+/
SUB_OP		/\-/
EQUAL_OP	/=/
LESS_THAN	/</
GREATER_THAN	/>/
NOT_GREATER	/<=/
NOT_LESS	/>=/
Delimiters
EOL		/\n\
EOF		/\Z/
Identifiers
IDENT		/[A-Za-z0-9_]{1,31}/
```

# The Scanner
The scanner tokenizes an input file of a valid BASIC code which follows the syntax of the subset. The tokens are represented as an enumerable type in Python using the enum library. The scanner processes the input file char by char and matches the regular expressions of the tokens to recognize them. The reGEX library is used to specify and match tokens in the scanner. The scanner is implemented as a class (Scanner) with a single public function lex() which is python generator of Token objects. Each Token object has a type, position (line and column), and lexeme. The type of token is a Tokens object which is an enumeration of all Tokens. The scanner also throws an error with the position when an unknown lexeme is encountered.

# The Parser 
A recursive-descent top-down parser implementation is implemented. We chose this approach due to the relatively simple grammar of our Basic subset and the implementation simplicity and extensibility this approach provides. Each non-terminal in the grammar is implemented as function and recursive calls of these functions is used to parse a program source file. The parser uses the scanner to retrieve tokens which are then parsed into valid statements in the Basic subset.   


# Running the Scanner with the Python Interpreter
The implementation of the scanner is in scanner.py while the subset is specified in basic_subset.py. When running the scanner, the python interpreter needs to be called with the source file name and the test file name of the BASIC source code:'

```python3 basic_scanner.py source_file_name.bas ```

# Running the Parser with the Python Interpreter
The implementation of the parser is in basic_parser.py which uses the scanner and Basic subset implemented in scanner.py and basic_subset.py. When running the parser, the python interpreter can be invoked with the source file name and the test file name (or path) of the BASIC source code: 

```python3 basic_parser.py source_file_name.bas ```

# Running the Interpreter with the Python Interpreter
The implementation of the interpreter is in basic_parser.py which uses the scanner, Basic subset, and the parser. When running the interpreter, the python interpreter can be invoked with the source file name and the test file name (or path) of the BASIC source code: 

```python3 basic_interpreter.py source_file_name.bas ```

