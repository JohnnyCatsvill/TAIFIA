
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

    "and": "binary_bool",
    "&&": "binary_bool",
    "||": "binary_bool",
    "or": "binary_bool",
    "!=": "binary_bool",
    "!": "unary_bool",
    "not": "unary_bool",
    "==": "binary_bool",
    "<=": "binary_bool",
    ">=": "binary_bool",
    "=": "assign",
    "<": "binary_bool",
    ">": "binary_bool",
    "+": "math_symbol",
    "-": "math_symbol",
    "*": "math_symbol",
    "//": "comment_start",
    "/": "math_symbol",
    "%": "math_symbol",
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