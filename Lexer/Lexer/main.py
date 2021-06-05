
from Lexer import *

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