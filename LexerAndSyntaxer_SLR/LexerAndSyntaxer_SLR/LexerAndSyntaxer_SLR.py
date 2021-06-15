
from Lexer import Lexer
from SLR1 import SLR_Table, CheckIfItSLR
from Runner import Runner
from TablePrinter import Print_2D_Table

def L_AND_S(rules, text):
    try:
        lex = Lexer(text)
        lex.run(show_states = False, show_spaces = False)
        #lex.show()
    
        table = SLR_Table(rules)
        #Print_2D_Table(table)
        CheckIfItSLR(table)
        
        lexer_list = [i for i in lex.list if i[1] != "new_line" and i[1] != "Comment"]
        lexer_list.append(["true_end", "$", "end_end"])
    
        Runner(table, lexer_list, rules)
    
    except Exception as e:
        print("Не подходит")
        print(e)
        return False
    else:
        print("Подходит")
        return True


rules = [
    ["PROGRAM", ["function_type entry_point bracket_smooth_l bracket_smooth_r bracket_curve_l LIST_OF_COMMANDS bracket_curve_r $"]],              
    
    ["LIST_OF_COMMANDS", ["COMMAND LIST_OF_COMMANDS"]],
    ["LIST_OF_COMMANDS", ["COMMAND"]],
    
    ["COMMAND", ["type ID divider"]],
    ["COMMAND", ["reader bracket_smooth_l ID bracket_smooth_r divider"]],
    ["COMMAND", ["printer bracket_smooth_l ID bracket_smooth_r divider"]],
    ["COMMAND", ["ID assign EXPRESSION divider"]],
    ["COMMAND", ["condition bracket_smooth_l CONDITION bracket_smooth_r bracket_curve_l LIST_OF_COMMANDS bracket_curve_r"]],
    ["COMMAND", ["condition bracket_smooth_l CONDITION bracket_smooth_r bracket_curve_l LIST_OF_COMMANDS bracket_curve_r condition_else bracket_curve_l LIST_OF_COMMANDS bracket_curve_r"]],
    ["COMMAND", ["cycle bracket_smooth_l CONDITION bracket_smooth_r bracket_curve_l LIST_OF_COMMANDS bracket_curve_r"]],
    
    ["ANY_NUMBER", ["OCT"]],
    ["ANY_NUMBER", ["HEX"]],
    ["ANY_NUMBER", ["BIN"]],
    ["ANY_NUMBER", ["FLOAT"]],
    ["ANY_NUMBER", ["ID"]],
    ["ANY_NUMBER", ["INT"]],

    ["EXPRESSION", ["EXPRESSION plus_symbol EXPRESSION2"]],
    ["EXPRESSION", ["EXPRESSION minus_symbol EXPRESSION2"]],
    ["EXPRESSION", ["EXPRESSION2"]],

    ["EXPRESSION2", ["EXPRESSION2 multiply_symbol EXPRESSION3"]],
    ["EXPRESSION2", ["EXPRESSION2 divide_symbol EXPRESSION3"]],
    ["EXPRESSION2", ["EXPRESSION3"]],

    ["EXPRESSION3", ["bracket_smooth_l EXPRESSION bracket_smooth_r"]],
    ["EXPRESSION3", ["minus_symbol EXPRESSION3"]],
    ["EXPRESSION3", ["ANY_NUMBER"]],

    ["CONDITION", ["CONDITION binary_or CONDITION2"]],
    ["CONDITION", ["CONDITION2"]],

    ["CONDITION2", ["CONDITION2 binary_and CONDITION3"]],
    ["CONDITION2", ["CONDITION3"]],

    ["CONDITION3", ["bracket_smooth_l CONDITION bracket_smooth_r"]],
    ["CONDITION3", ["unary_not CONDITION3"]],
    ["CONDITION3", ["boolean_true"]],
    ["CONDITION3", ["boolean_false"]],
    ["CONDITION3", ["ANY_NUMBER binary_compare ANY_NUMBER"]]
]

program_text = open("program.txt", "r").read()
L_AND_S(rules, program_text)
