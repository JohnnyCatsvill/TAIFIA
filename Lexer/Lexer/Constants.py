
dictionary = {
    "void": "function_type",
    "int": "type",
    "float": "type",
    "string": "type",
    "char": "type",
    "bool":  "type",
    "hex": "type",
    "oct": "type",
    "bin": "type",
    "fixed": "type",
    
    "main": "entry_point",
    "(": "bracket_smooth_l",
    ")": "bracket_smooth_r",
    "{": "bracket_curve_l",
    "}": "bracket_curve_r",
    "[": "bracket_rect_l",
    "]": "bracket_rect_r",
    ";": "divider",
    "read": "reader",
    "print": "printer",

    "true": "boolean_true",
    "True": "boolean_true",
    "false": "boolean_false",
    "False": "boolean_false",

    "and": "binary_and",
    "&&": "binary_and",
    "||": "binary_or",
    "or": "binary_or",
    "!=": "binary_compare",
    "!": "unary_not",
    "not": "unary_not",
    "==": "binary_compare",
    "<=": "binary_compare",
    ">=": "binary_compare",
    "=": "assign",
    "<": "binary_compare",
    ">": "binary_compare",
    "+": "plus_symbol",
    "-": "minus_symbol",
    "*": "multiply_symbol",
    "//": "comment_start",
    "/": "divide_symbol",
    "%": "mod_symbol",
    ",": "comma",
    " ": "separator",
    "\n": "new_line",
    
    "if": "condition",
    "else": "condition_else",
    "while": "cycle"
}

LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
SYMBOLS = "(){}[];=<>!+-*/%, "
NUMBERS = "0123456789"
STOP_POINTS = " (){}[];=<>!+-*/%,\n"

BIN = "01"
OCT = "01234567"
HEX = "0123456789abcdefABCDEF"

HEX_START = "x"
BIN_START = "b"

POINT = "."

ROW_NAME = "Row "
ROW_COL_DIVIDER_NAME = " / "
COLUMN_NAME = "Col "

WORD_TO_TYPE_DELIMER = ""
ERROR_NAME = "ERR"
COMMENT_NAME = "Comment"
ID_NAME = "ID"
HEX_NAME = "HEX"
OCT_NAME = "OCT"
BIN_NAME = "BIN"
DEC_NAME = "INT"
FLOAT_NAME = "FLOAT"

MAX_LENGTH_OF_TYPES = {
    DEC_NAME: 11,
    ID_NAME: 64
}