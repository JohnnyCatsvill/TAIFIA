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
    
    while(i < 10) //cycle
    {
        i = i + 1;
    }
}

"""

lex = Lexer(program_text)
lex.run(show_states = False, show_spaces = False)
lex.show()


rules = [
    ["PROGRAM", ["function_type entry_point bracket_smooth_l bracket_smooth_r bracket_curve_l LIST_OF_COMMANDS bracket_curve_r $"]],              
    
    ["LIST_OF_COMMANDS", ["COMMAND LIST_OF_COMMANDS"]],
    ["LIST_OF_COMMANDS", ["COMMAND"]],
    
    ["COMMAND", ["type ID divider"]],
    
    ["COMMAND", ["reader bracket_smooth_l ID bracket_smooth_r divider"]],
    ["COMMAND", ["printer bracket_smooth_l ID bracket_smooth_r divider"]],

    ["COMMAND", ["ID assign EXPRESSION divider"]],
    
    ["COMMAND", ["condition bracket_smooth_l CONDITION_LIST bracket_smooth_r bracket_curve_l LIST_OF_COMMANDS bracket_curve_r"]],
    ["COMMAND", ["condition bracket_smooth_l CONDITION_LIST bracket_smooth_r bracket_curve_l LIST_OF_COMMANDS bracket_curve_r condition_else bracket_curve_l LIST_OF_COMMANDS bracket_curve_r"]],
    
    ["CONDITION_LIST", ["bracket_smooth_l CONDITION_LIST bracket_smooth_r binary_bool bracket_smooth_l CONDITION_LIST bracket_smooth_r"]],
    ["CONDITION_LIST", ["CONDITION_LIST binary_bool CONDITION_LIST"]],
    ["CONDITION_LIST", ["unary_bool CONDITION_LIST"]],
    ["CONDITION_LIST", ["unary_bool bracket_smooth_l CONDITION_LIST bracket_smooth_r"]],
    ["CONDITION_LIST", ["ID"]],
    ["CONDITION_LIST", ["INT"]],
    ["CONDITION_LIST", ["OCT"]],
    ["CONDITION_LIST", ["HEX"]],
    ["CONDITION_LIST", ["BIN"]],
    ["CONDITION_LIST", ["FLOAT"]],
    
    ["COMMAND", ["cycle bracket_smooth_l CONDITION_LIST bracket_smooth_r bracket_curve_l LIST_OF_COMMANDS bracket_curve_r"]],

    ["ANY_NUMBER", ["INT", "OCT", "HEX", "BIN", "FLOAT", "ID"]],
    ["EXPRESSION", ["EXPRESSION math_symbol EXPRESSION"]],
    ["EXPRESSION", ["bracket_smooth_l EXPRESSION bracket_smooth_r math_symbol bracket_smooth_l EXPRESSION bracket_smooth_r"]],
    ["EXPRESSION", ["ANY_NUMBER"]]

    
]

table = Run(rules, lr_letter="LevRecur", ft_letter="Factor", word = "", show_all = False)

runner = Runner_cl(1, table, "$")

for i in lex.list:
    if i[1] != "new_line" and i[1] != "Comment":
        runner.Run(i[1], i[2])

is_end = runner.Run("$", "end_end")
if is_end:
    print("EVERYTHING IS FINE, BUT MY MENTAL HEALTH")
else:
    print("WERE F**CKED")