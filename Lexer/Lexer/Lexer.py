from Constants import *

class Lexer(object):
    
    def __init__(self, program_text):
        self.text = program_text + "\n"
        self.list = []
    
        
    def run(self, show_states = False, show_spaces = False):
        
        def state_error(symbol, word, row, column):
            if symbol in STOP_POINTS:
                self.list.append([word[0], WORD_TO_TYPE_DELIMER + ERROR_NAME, ROW_NAME + str(row) + ROW_COL_DIVIDER_NAME + COLUMN_NAME + str(column)])
                word[0] = ""
                return state_start(symbol, word, row, column)
            else:
                return state_error
            
        def state_unary_stop_symbol(symbol, word, row, column):
            if dictionary.get(word[0], False):
                if word[0] == " " and not show_spaces:
                    pass
                else:    
                    self.list.append([word[0], WORD_TO_TYPE_DELIMER + dictionary[word[0]], ROW_NAME + str(row) + ROW_COL_DIVIDER_NAME + COLUMN_NAME + str(column)])
            word[0] = ""
            return state_start(symbol, word, row, column)
        
        def state_undefined_stop_symbol(symbol, word, row, column):
            if symbol == "=":
                return state_dual_stop_symbol
            else:
                if dictionary.get(word[0], False):
                    self.list.append([word[0], WORD_TO_TYPE_DELIMER + dictionary[word[0]], ROW_NAME + str(row) + ROW_COL_DIVIDER_NAME + COLUMN_NAME + str(column)])
                word[0] = ""
                return state_start(symbol, word, row, column)
            
        def state_dual_stop_symbol(symbol, word, row, column):
            if dictionary.get(word[0], False):
                self.list.append([word[0], WORD_TO_TYPE_DELIMER + dictionary[word[0]], ROW_NAME + str(row) + ROW_COL_DIVIDER_NAME + COLUMN_NAME + str(column)])
            word[0] = ""
            return state_start(symbol, word, row, column)
        
        def state_slash_symbol(symbol, word, row, column):
            if symbol == "/":
                return state_comment
            elif symbol == "*":
                return state_multi_comment
            else:
                if dictionary.get(word[0], False):
                    self.list.append([word[0], WORD_TO_TYPE_DELIMER + dictionary[word[0]], ROW_NAME + str(row) + ROW_COL_DIVIDER_NAME + COLUMN_NAME + str(column)])
                word[0] = ""
                return state_start(symbol, word, row, column)
        
        def state_comment(symbol, word, row, column):
            if symbol == "\n":
                self.list.append([word[0], WORD_TO_TYPE_DELIMER + COMMENT_NAME, ROW_NAME + str(row) + ROW_COL_DIVIDER_NAME + COLUMN_NAME + str(column)])
                word[0] = ""
                return state_start(symbol, word, row, column)
            else:
                return state_comment
            
        def state_multi_comment(symbol, word, row, column):
            if symbol == "*":
                return state_multi_comment_exit
            else:
                return state_multi_comment
            
        def state_multi_comment_exit(symbol, word, row, column):
            if symbol == "/":
                self.list.append([word[0] + "/", WORD_TO_TYPE_DELIMER + COMMENT_NAME, ROW_NAME + str(row) + ROW_COL_DIVIDER_NAME + COLUMN_NAME + str(column)])
                word[0] = ""
                return state_start
            else:
                return state_multi_comment
            
                
        def state_identifier(symbol, word, row, column):   
            if symbol in LETTERS + NUMBERS + "_":
                return state_identifier
            else:
                if dictionary.get(word[0], False):
                    self.list.append([word[0], WORD_TO_TYPE_DELIMER + dictionary[word[0]], ROW_NAME + str(row) + ROW_COL_DIVIDER_NAME + COLUMN_NAME + str(column)])
                else:
                    self.list.append([word[0], WORD_TO_TYPE_DELIMER + ID_NAME, ROW_NAME + str(row) + ROW_COL_DIVIDER_NAME + COLUMN_NAME + str(column)])
                word[0] = ""
                return state_start(symbol, word, row, column)
            
        def state_hex_number(symbol, word, row, column):
            if symbol in HEX:
                return state_hex_number
            elif symbol in NUMBERS + LETTERS:
                return state_error(symbol, word, row, column)
            else:
                self.list.append([word[0], WORD_TO_TYPE_DELIMER + HEX_NAME, ROW_NAME + str(row) + ROW_COL_DIVIDER_NAME + COLUMN_NAME + str(column)])
                word[0] = ""
                return state_start(symbol, word, row, column)
            
        def state_bin_number(symbol, word, row, column):
            if symbol in BIN:
                return state_bin_number
            elif symbol in NUMBERS + LETTERS:
                return state_error(symbol, word, row, column)
            else:
                self.list.append([word[0], WORD_TO_TYPE_DELIMER + BIN_NAME, ROW_NAME + str(row) + ROW_COL_DIVIDER_NAME + COLUMN_NAME + str(column)])
                word[0] = ""
                return state_start(symbol, word, row, column)
            
        def state_oct_number(symbol, word, row, column):
            if symbol in OCT:
                return state_oct_number
            elif symbol in NUMBERS + LETTERS:
                return state_error(symbol, word, row, column)
            else:
                self.list.append([word[0], WORD_TO_TYPE_DELIMER + OCT_NAME, ROW_NAME + str(row) + ROW_COL_DIVIDER_NAME + COLUMN_NAME + str(column)])
                word[0] = ""
                return state_start(symbol, word, row, column)
            
        def state_float(symbol, word, row, column):
            if symbol in NUMBERS:
                return state_float
            elif symbol in "eE":
                return state_float_exponent
            elif symbol in LETTERS:
                return state_error(symbol, word, row, column) 
            else:
                self.list.append([word[0], WORD_TO_TYPE_DELIMER + FLOAT_NAME, ROW_NAME + str(row) + ROW_COL_DIVIDER_NAME + COLUMN_NAME + str(column)])
                word[0] = ""
                return state_start(symbol, word, row, column)
            
        def state_undefined_float(symbol, word, row, column):
            if symbol in NUMBERS:
                return state_float
            elif symbol in LETTERS:
                return state_error(symbol, word, row, column) 
            else:
                return state_error(symbol, word, row, column)
            
        def state_float_exponent(symbol, word, row, column):
            if symbol in "+-":
                return state_float_exponent_sign
            else:
                return state_error
            
        def state_float_exponent_sign(symbol, word, row, column):
            if symbol in "123456789":
                return state_float_exponent_numbers
            elif symbol in "0":
                return state_float_exponent_zero
            else:
                return state_error
            
        def state_float_exponent_numbers(symbol, word, row, column):
            if symbol in "0123456789":
                return state_float_exponent_numbers
            elif symbol in LETTERS:
                return state_error(symbol, word, row, column) 
            else:
                self.list.append([word[0], WORD_TO_TYPE_DELIMER + FLOAT_NAME, ROW_NAME + str(row) + ROW_COL_DIVIDER_NAME + COLUMN_NAME + str(column)])
                word[0] = ""
                return state_start(symbol, word, row, column)
            
        def state_float_exponent_zero(symbol, word, row, column):
            if symbol in LETTERS + NUMBERS:
                return state_error(symbol, word, row, column) 
            else:
                self.list.append([word[0], WORD_TO_TYPE_DELIMER + FLOAT_NAME, ROW_NAME + str(row) + ROW_COL_DIVIDER_NAME + COLUMN_NAME + str(column)])
                word[0] = ""
                return state_start(symbol, word, row, column)
        
        def state_any_number(symbol, word, row, column):
            if symbol == HEX_START:
                return state_hex_number
            elif symbol == BIN_START:
                return state_bin_number
            elif symbol in OCT:
                return state_oct_number
            elif symbol == POINT:
                return state_float
            elif symbol in NUMBERS + LETTERS:
                return state_error(symbol, word, row, column)
            else:
                self.list.append([word[0], WORD_TO_TYPE_DELIMER + DEC_NAME, ROW_NAME + str(row) + ROW_COL_DIVIDER_NAME + COLUMN_NAME + str(column)])
                word[0] = ""
                return state_start(symbol, word, row, column)
            
        def state_int_or_float(symbol, word, row, column):
            if symbol in NUMBERS:
                return state_int_or_float
            elif symbol == POINT:
                return state_float
            elif symbol in LETTERS:
                return state_error(symbol, word, row, column)
            else:
                self.list.append([word[0], WORD_TO_TYPE_DELIMER + DEC_NAME, ROW_NAME + str(row) + ROW_COL_DIVIDER_NAME + COLUMN_NAME + str(column)])
                word[0] = ""
                return state_start(symbol, word, row, column)
        
        def state_start(symbol, word, row, column):
            if symbol in LETTERS:
                return state_identifier
            elif symbol == "/":
                return state_slash_symbol
            elif symbol in "<>!=":
                return state_undefined_stop_symbol
            elif symbol in "(){}[];+-*%, \n":
                return state_unary_stop_symbol
            elif symbol in "123456789":
                return state_int_or_float
            elif symbol == "0":
                return state_any_number
            elif symbol == ".":
                return state_undefined_float
            else:
                return state_error
            
        def check_for_type_length_limit():
            for i in self.list: 
                if i[1] in MAX_LENGTH_OF_TYPES:
                    if len(i[0]) > MAX_LENGTH_OF_TYPES[i[1]]:
                        i[1] = ERROR_NAME
            
        state = state_start
        word = [""]
    
        row = 0
        column = -1
        last_symbol = ""
        for i in self.text:
            new_state = state(i, word, row, column)
            
            if show_states:
                print(new_state, i)
            
            word[0] = word[0] + i
            
            state = new_state
            
            if last_symbol == "\n":
                row = row + 1
                column = 0
            else:
                column = column + 1
                
            last_symbol = i
            
        check_for_type_length_limit()
            
    def show(self):
        for i in self.list:
            print(i)