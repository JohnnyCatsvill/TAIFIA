from Lexer import Lexer
from LL1 import Run, Runner_cl

program_text = """

void main()
{
    int i;    //init
    float f;
    string s;
    bool b;
    
    hex h;
    oct o;
    bin bit;
    fixed fix;
    
    read(s);   //read write
    print( s );
    
    i = 06;    //assign
    i =0x7;
    i= 0b01;
    i=6;
    f = 0.50;
    
    if(i == 6  or i==5 and i!= 6 and i<=5)  //condition
    {
        i = 5;
    }

    else /* I want multicomment here
    and noone can stop me 
    do this */
    {
        i = 6;
    }

    if (i == 5)
    {
        i = 2 + 3 + 28 + 2.85;
    }
    else
    {
        i = 2;
    }
    
    while(i < 10) //cycle
    {
        i = i + 1;
    }
}

"""



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

    ["BINARY_PLUS_MINUS", ["plus_symbol", "minus_symbol"]],

    ["EXPRESSION", ["EXPRESSION plus_symbol EXPRESSION2"]],
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

def L_AND_S(rules, text):
    try:
        lex = Lexer(text)
        lex.run(show_states = False, show_spaces = False)
        #lex.show()
    
        table = Run(rules, lr_letter="LR", ft_letter="FR", word = "", show_all = False)
        
        runner = Runner_cl(1, table, "$")
        
        for i in lex.list:
            if i[1] != "new_line" and i[1] != "Comment":
                runner.Run(i[1], i[2])
                #print(runner.pos_stack)
        
        is_end = runner.Run("$", "end_end")
        if not is_end:
            raise Exception("Промахнулись с концом", runner.current_pos, runner.pos_stack)
    
    except Exception as e:
        print("Не подходит")
        print(e)
    else:
        print("Подходит")

L_AND_S(rules, program_text)