
END_SYMBOL = "$"

def ParseRule(rule, divider = " "):
    rule_list = rule.split(divider)
    return rule_list

def Runner(slr_table, input_mass, rules):

    empty_symbol = "e"
    dict_of_rule_length = {i+1: len(ParseRule(rules[i][1][0])) - (1 if i == 0 or ParseRule(rules[i][1][0])[0] == empty_symbol else 0) for i in range(len(rules))}
    dict_of_rule_letters = {i+1: rules[i][0] for i in range(len(rules))}

    input_stack = [i for i in input_mass[::-1]]
    left_stack = []
    right_stack = [rules[0][0]]

    #print("разбор  INPUT-", input_stack, "  RIGHT-" , right_stack, "  LEFT-", left_stack)

    while right_stack[-1] != "OK":
        for row in slr_table:
            if row[0] == right_stack[-1]:
                cell_num = 0
                for cell_num in range(1, len(slr_table[0])):
                    if slr_table[0][cell_num] == input_stack[-1][1]:
                        if row[cell_num] == []:
                            #print(input_stack[-1][0] + " " + input_stack[-1][1] + " " + input_stack[-1][2] + " неожиданный символ")
                            raise Exception("Unexpected symbol", "символ {} попался вне контекста текущих символов".format(input_stack[-1]))
                            
                        else:
                            
                            if len(row[cell_num]) > 1:
                                parsed_multiple = ", ".join(row[cell_num])
                                left_stack.append(input_stack.pop())
                                right_stack.append(parsed_multiple)
                            else:
                                if len(ParseRule(row[cell_num][0])) == 2:
                                    
                                    for i in range(dict_of_rule_length[int(ParseRule(row[cell_num][0])[1])]):
                                        left_stack.pop()
                                        right_stack.pop()
                                    input_stack.append([input_stack[-1][0], dict_of_rule_letters[int(ParseRule(row[cell_num][0])[1])], input_stack[-1][2]])
                                else:
                                    left_stack.append(input_stack.pop())
                                    right_stack.append(row[cell_num][0])
                        cell_num = cell_num - 1
                        break
                if cell_num + 1 == len(slr_table[0]):
                    raise Exception("Unexpected symbol", "символ {} не из текущей грамматики".format(input_stack[-1]))
                    #print("НЕ ПОДХОДИТ, {} символа нет в таблице".format(input_stack[-1]))
                    #exit(0)
                break
        #print()
    

    if left_stack == [['true_end', rules[0][0], 'end_end']] and input_stack == [['true_end', END_SYMBOL, 'end_end']] and right_stack == [rules[0][0], "OK"]:
        #print("ПОДХОДИТ")
        return True
    else:
        raise Exception("Non empty stack", "какие-то символы были упущены, вот стек: \n \n input: {} \n \n left: {} \n \n right: {}".format(input_stack, right_stack, left_stack))
        #print("разбор  INPUT-", input_stack, "\n  RIGHT-" , right_stack, "\n  LEFT-", left_stack, "\n")
        