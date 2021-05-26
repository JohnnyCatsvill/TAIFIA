from TablePrinter import *

def ParseRule(rule, divider = " "):
    rule_list = rule.split(divider)
    return rule_list

def First(rules):
    set_of_nonterminals = set([rule_pack[0] for rule_pack in rules])
    empty_symbol = "e"
    end_symbol = "$"
    set_of_control_symbols = {empty_symbol, end_symbol}
    set_of_terminals = set([ letter for rule_pack in rules for letter in ParseRule(rule_pack[1][0]) if letter not in set_of_nonterminals and letter not in set_of_control_symbols ])

    first_table = {i: [] for i in set_of_nonterminals}
    empty_table = {i: [] for i in set_of_nonterminals}
    #for rule_pack_num in range(len(rules)):
    #    for letter_num in range(len(ParseRule(rules[rule_pack_num][1][0]))):
    #        letter = ParseRule(rules[rule_pack_num][1][0])[letter_num]
    #        first_table[letter + " " + str(rule_pack_num) + " " + str(letter_num)] = []
    last_table = {"why": "i dont understand!!!, <sobs>"}

    while first_table != last_table:
        last_table = copy.deepcopy(first_table)
        for rule_pack_num in range(len(rules)):
            rule_pack = rules[rule_pack_num]
            first_letter = rule_pack[1][0][0]
            cur_nonterm = rule_pack[0]

            if cur_nonterm not in first_table:
                first_table[cur_nonterm] = []
            if cur_nonterm not in first_table:
                empty_table[cur_nonterm] = []
                #weak_first_table[cur_nonterm] = []

            if first_letter in set_of_nonterminals:
                if first_letter + " " + str(rule_pack_num+1) + " " + "1" not in first_table[cur_nonterm]:
                    first_table[cur_nonterm].append(first_letter + " " + str(rule_pack_num+1) + " " + "1")
                if first_letter in first_table:
                    for i in first_table[first_letter]:
                        if i not in first_table[cur_nonterm]:
                            first_table[cur_nonterm].append(i)

            elif first_letter in set_of_terminals:
                if first_letter + " " + str(rule_pack_num+1) + " " + "1" not in first_table[cur_nonterm]:
                    first_table[cur_nonterm].append(first_letter + " " + str(rule_pack_num+1) + " " + "1")

            elif first_letter == empty_symbol:
                afterlooking_symbols = {cur_nonterm}
                afterlooking_symbols_old = set()
            
                while afterlooking_symbols != afterlooking_symbols_old:
                    afterlooking_symbols_old = afterlooking_symbols
                    for new_rule_pack_num in range(len(rules)):
                        new_rule_pack = rules[new_rule_pack_num]
                        parsed_rule = ParseRule(new_rule_pack[1][0])
                        for letter_num in range(len(parsed_rule)):
                            letter = parsed_rule[letter_num]
                            if letter in afterlooking_symbols:
                                
                                if letter_num + 1 < len(parsed_rule):
                                    next_letter = parsed_rule[letter_num + 1]
                                    if next_letter + " " + str(new_rule_pack_num+1) + " " + str(letter_num+2) + " " + str(rule_pack_num+1) not in empty_table[cur_nonterm]:
                                        if new_rule_pack[0] != cur_nonterm:
                                            #first_table[cur_nonterm].append(next_letter + " " + str(new_rule_pack_num+1) + " " + str(letter_num+2))
                                            empty_table[cur_nonterm].append(next_letter + " " + str(new_rule_pack_num+1) + " " + str(letter_num+2) + " " + str(rule_pack_num+1))
                                            
                                    if next_letter in first_table:
                                        for i in first_table[next_letter]:
                                            if i + " " + str(rule_pack_num+1) not in empty_table[cur_nonterm]:
                                                #first_table[cur_nonterm].append(i)
                                                empty_table[cur_nonterm].append(i + " " + str(rule_pack_num+1))
                                else:
                                    afterlooking_symbols.add(new_rule_pack[0])
            


            #print(first_table)
            #print()
        #
    #for i, j in first_table.items():
    #    print(i, "-> ", j)
    #
    #print()
    #
    #for i, j in empty_table.items():
    #    print(i, "-> ", j)
    #
    #
    #print()
    return [first_table, empty_table]
        
def Follow(rules):
    first_table_ = First(rules)
    first_table = first_table_[0]
    empty_table = first_table_[1]

    set_of_nonterminals = set([rule_pack[0] for rule_pack in rules])
    set_of_empty_nonterminals = {rules[rule_pack_num][0] : str(rule_pack_num+1) for rule_pack_num in range(len(rules)) if rules[rule_pack_num][1][0] == "e"}
    
    #print(dict_of_rule_length, "rulelength")

    #print(set_of_empty_nonterminals, "emptynonternms")
    empty_symbol = "e"
    end_symbol = "$"
    set_of_control_symbols = {empty_symbol}
    set_of_terminals = set([ letter for rule_pack in rules for letter in ParseRule(rule_pack[1][0]) if letter not in set_of_nonterminals and letter not in set_of_control_symbols ])

    follow_table = dict()
    for rule_pack_num in range(len(rules)):
        for letter_num in range(len(ParseRule(rules[rule_pack_num][1][0]))):
            letter = ParseRule(rules[rule_pack_num][1][0])[letter_num]
            follow_table[letter + " " + str(rule_pack_num+1) + " " + str(letter_num+1)] = []
    last_table = {"why": "i dont understand!!!, <sobs>"}
    follow_table[rules[0][0]] = []

    while follow_table != last_table:
        last_table = copy.deepcopy(follow_table)

        first_nonterm = rules[0][0]
        first_first_symbol = ParseRule(rules[0][1][0])[0]
        follow_letter = follow_table[first_nonterm]

        parsed_rule = ParseRule(rules[0][1][0])
        next_letter = parsed_rule[0]

        if first_first_symbol in set_of_terminals:
            if first_first_symbol + " 1 1" not in follow_letter:
                follow_letter.append(first_first_symbol + " 1 1")
        elif first_first_symbol in set_of_nonterminals:
            if first_first_symbol + " 1 1" not in follow_letter:
                if first_first_symbol in first_table[first_first_symbol]:
                    follow_letter.append(first_first_symbol + " 1 1")
                else:
                    follow_letter.append(first_first_symbol + " 1 1")
            for i in first_table[first_first_symbol]:
                if i not in follow_letter:
                    follow_letter.append(i)
            #for i in empty_table[first_first_symbol]:
            #    if i not in follow_letter:
            #        follow_letter.append(i)
            if next_letter + " 1 1" in follow_table and next_letter in set_of_empty_nonterminals:
                for i in follow_table[next_letter + " 1 1"]:
                    if i + " " + set_of_empty_nonterminals[next_letter] not in follow_letter:
                        follow_letter.append(i + " " + set_of_empty_nonterminals[next_letter])


        for rule_pack_num in range(len(rules)):
            rule_pack = rules[rule_pack_num]
            cur_nonterm = rule_pack[0]
            parsed_rule = ParseRule(rule_pack[1][0])

            for letter_num in range(len(parsed_rule)):
                letter = parsed_rule[letter_num]
                follow_letter = follow_table[letter + " " + str(rule_pack_num+1) + " " + str(letter_num+1)]
                #if letter in set_of_nonterminals:
                if letter_num + 1 < len(parsed_rule):
                    next_letter = parsed_rule[letter_num + 1]


                    if next_letter in set_of_terminals:
                        if next_letter + " " + str(rule_pack_num+1) + " " + str(letter_num+2) not in follow_letter:
                            follow_letter.append(next_letter + " " + str(rule_pack_num+1) + " " + str(letter_num+2))

                    elif next_letter in set_of_nonterminals:
                        if next_letter + " " + str(rule_pack_num+1) + " " + str(letter_num+2) not in follow_letter:
                            follow_letter.append(next_letter + " " + str(rule_pack_num+1) + " " + str(letter_num+2))

                        for i in first_table[next_letter]:
                            if i not in follow_letter:
                                follow_letter.append(i)
                        #for i in empty_table[next_letter]:
                        #    if i not in follow_letter:
                        #        follow_letter.append(i)
                        if next_letter + " " + str(rule_pack_num+1) + " " + str(letter_num+2) in follow_table and next_letter in set_of_empty_nonterminals:
                            for i in follow_table[next_letter + " " + str(rule_pack_num+1) + " " + str(letter_num+2)]:
                                if i + " " + set_of_empty_nonterminals[next_letter] not in follow_letter:
                                    follow_letter.append(i + " " + set_of_empty_nonterminals[next_letter])
                   


                elif letter != empty_symbol:
                    for i in follow_table:
                        splits = i.split(" ")
                        if splits[0] == cur_nonterm:
                            for j in follow_table[i]:
                                if j not in follow_letter:
                                    follow_letter.append(j)

    
    


    items_to_delete = []
    for i, j in follow_table.items():
        if ParseRule(i)[0] == empty_symbol or ParseRule(i)[0] == end_symbol:
            items_to_delete.append(i)

    for i in items_to_delete:
        follow_table.pop(i)


    #for i, j in follow_table.items():
    #    print(i, "-> ", j)
    #print()

    return follow_table



def SLR_Table(rules):
    follow_table = Follow(rules)

    empty_symbol = "e"
    end_symbol = "$"
    set_of_control_symbols = {empty_symbol, end_symbol}
    
    set_of_nonterminals = []
    for rule_pack in rules:
        if rule_pack[0] not in set_of_nonterminals:
            set_of_nonterminals.append(rule_pack[0])
    
    set_of_terminals = []
    for rule_pack in rules:
        for letter in ParseRule(rule_pack[1][0]):
            if letter not in set_of_nonterminals and letter not in set_of_control_symbols and letter not in set_of_terminals:
                set_of_terminals.append(letter)


    slr_table = [[i for i in [""] + set_of_nonterminals + list(set_of_terminals) + [end_symbol]]]
    

    for letter, follow in follow_table.items():
        thing_to_append = [[] for i in slr_table[0][1:]]
        thing_to_append.insert(0, letter)
        #print(thing_to_append)
        for i in range(1, len(slr_table[0])):
            for j in range(len(follow)):
                j_letter = follow[j]
                if slr_table[0][i] == ParseRule(j_letter)[0]:

                    if len(ParseRule(letter)) == 1 or len(ParseRule(rules[int(ParseRule(letter)[1])-1][1][0])) > int(ParseRule(letter)[2]) + (1 if ParseRule(letter)[1] == "1" else 0):
                        if j_letter not in thing_to_append[i]:
                            #if ParseRule(j_letter)[0] != end_symbol:
                                thing_to_append[i].append(j_letter)
                            #else:
                            #    thing_to_append[i].append("R" + ParseRule(j_letter)[1])
                        if len(ParseRule(letter)) == 1:
                            if "OK" not in thing_to_append[1]:
                                thing_to_append[1].append("OK")

                    else:
                        if "R " + ParseRule(letter)[1] not in thing_to_append[i]:
                            thing_to_append[i].append("R " + ParseRule(letter)[1])
                    
        #print(thing_to_append)
        slr_table.append(thing_to_append)

    for row in slr_table[1:]:
        for cell_num in range(1, len(row)):
            cell = row[cell_num]
            new_cell = []
            for letter_num in range(len(cell)):
                if len(ParseRule(cell[letter_num])) > 3:
                    if "R " + ParseRule(cell[letter_num])[-1] not in new_cell:
                        new_cell.append("R " + ParseRule(cell[letter_num])[-1])
                else:
                    new_cell.append(cell[letter_num])
                    #cell[letter_num] = "R" + ParseRule(cell[letter_num])[-1]
                    
                        
            row[cell_num] = new_cell

    for row in slr_table[1:]:
        for cell in row[1:]:
            if len(cell) > 1:
                #print(cell)
                new_row_name = ", ".join(cell)
                
                need_to_do = True

                for i in slr_table:
                    if new_row_name == i[0]:
                        need_to_do = False

                if need_to_do:

                    thing_to_append = [[] for i in slr_table[0][1:]]
                    thing_to_append.insert(0, new_row_name)

                    for needed_rows in cell:
                        for rows in slr_table:
                            if rows[0] == needed_rows:
                                for cells_num in range(1, len(rows)):
                                    for cell_items in rows[cells_num]:

                                        thing_to_append[cells_num].append(cell_items)

                    slr_table.append(thing_to_append)

            #for letter_num in range(len(cell)):
            #    if len(ParseRule(cell[letter_num])) > 3:
            #        cell[letter_num] = "R" + ParseRule(cell[letter_num])[-1]
    
    Print_2D_Table(slr_table)
    #print(slr_table)
    return slr_table       

def Runner(slr_table, input, rules):

    empty_symbol = "e"
    dict_of_rule_length = {i+1: len(ParseRule(rules[i][1][0])) - (1 if i == 0 or ParseRule(rules[i][1][0])[0] == empty_symbol else 0) for i in range(len(rules))}
    dict_of_rule_letters = {i+1: rules[i][0] for i in range(len(rules))}

    input_stack = [i for i in input[::-1]]
    left_stack = []
    right_stack = [rules[0][0]]

    print("разбор  INPUT-", input_stack, "  RIGHT-" , right_stack, "  LEFT-", left_stack)

    while right_stack[-1] != "OK":
        for row in slr_table:
            if row[0] == right_stack[-1]:
                cell_num = 0
                for cell_num in range(1, len(slr_table[0])):
                    if slr_table[0][cell_num] == input_stack[-1]:
                        if row[cell_num] == []:
                            print("НЕ ПОДХОДИТ, И ДА КРАШИМСЯ")
                            exit(0)
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
                                    input_stack.append(dict_of_rule_letters[int(ParseRule(row[cell_num][0])[1])])
                                else:
                                    left_stack.append(input_stack.pop())
                                    right_stack.append(row[cell_num][0])
                        cell_num = cell_num - 1
                        break
                if cell_num + 1 == len(slr_table[0]):
                    print("НЕ ПОДХОДИТ, И ДА КРАШИМСЯ")
                    exit(0)
                break
        print()
        print("разбор  INPUT-", input_stack, "  RIGHT-" , right_stack, "  LEFT-", left_stack)


    if left_stack == [rules[0][0]]:
        print("ПОДХОДИТ")
    else:
        print("НЕ ПОДХОДИТ")





RULES = [
    ["Z", ["S $"]],
    ["S", ["( S )"]],
    ["S", ["e"]]
    ]

Print_2D_Table(RULES)
Runner(SLR_Table(RULES), "(())$", RULES)
print()
print("///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
print()

RULES = [
    ["S", ["A B C $"]],
    ["A", ["a A"]],
    ["A", ["e"]],
    ["B", ["b B"]],
    ["B", ["b"]],
    ["C", ["c C"]],
    ["C", ["c"]]
    ]

Print_2D_Table(RULES)
Runner(SLR_Table(RULES), "aaabbc$", RULES)
print()
print("///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
print()

RULES = [
    ["S", ["A B C $"]],
    ["A", ["a A"]],
    ["A", ["e"]],
    ["B", ["b B"]],
    ["B", ["e"]],
    ["C", ["c C"]],
    ["C", ["e"]]
    ]

Print_2D_Table(RULES)
Runner(SLR_Table(RULES), "aaabbc$", RULES)
print()
print("///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
print()

RULES = [
    ["Z", ["A $"]],
    ["A", ["A * B"]],
    ["A", ["B"]],
    ["B", ["( A )"]],
    ["B", ["i"]]
    ]

Print_2D_Table(RULES)
SLR_Table(RULES)
print()
print("///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
print()

RULES = [
    ["Z", ["S $"]],
    ["S", ["( S )"]],
    ["S", ["( )"]]
    ]

Print_2D_Table(RULES)
Runner(SLR_Table(RULES), "(())$", RULES)
print()
print("///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
print()