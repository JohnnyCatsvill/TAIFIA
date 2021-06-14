
from TablePrinter import Print_2D_Table
import copy

def ParseRule(rule, divider = " "):
    rule_list = rule.split(divider)
    return rule_list

def UniformRules(unfixed_rules):
    # просто задать более укомплектованный вид правилам, более легкие в обращении
    new_rules = []
    current_nonterminal = ""
    current_nonterminal_rules = []

    copy_of_unfixed_rules = copy.deepcopy(unfixed_rules)
    
    for rule in copy_of_unfixed_rules:
        if rule[0] != current_nonterminal:
            
            if current_nonterminal != "":
                new_rules.append([current_nonterminal, current_nonterminal_rules])
            
            current_nonterminal = rule[0]
            current_nonterminal_rules = rule[1]
            
        else:
            for i in rule[1]:
                current_nonterminal_rules.append(i) 
            
    new_rules.append([current_nonterminal, current_nonterminal_rules])
    
    return new_rules

def RemoveLeftRecursion(unfixed_rules, new_letter):
    
    NEW_LETTER_START = new_letter
    new_rules = []
    new_letter_num = 1
    
    for rule_pack in UniformRules(unfixed_rules):
        
        current_nonterminal = rule_pack[0]
        recursive_rules = []
        non_recursive_rules = []
        
        for rule in rule_pack[1]: #поиск рекурсии
            
            if current_nonterminal in ParseRule(rule):
                recursive_rules.append(rule)
            else:
                non_recursive_rules.append(rule)
              
        if len(non_recursive_rules) > 0: 
            if len(recursive_rules) > 0: #проверка на рекурсию
                
                for j in non_recursive_rules:
                    new_rules.append([current_nonterminal, [j + " " + current_nonterminal + "_" + NEW_LETTER_START + str(new_letter_num)]])
                
                for j in recursive_rules:
                    new_rules.append([current_nonterminal + "_" + NEW_LETTER_START + str(new_letter_num), [j.replace(current_nonterminal, "", 1).replace(" ", "", 1) + " " + current_nonterminal + "_" + NEW_LETTER_START + str(new_letter_num)]])
                new_rules.append([current_nonterminal + "_" + NEW_LETTER_START + str(new_letter_num), ["e"]])
                
                
            
            else:
                new_rules.append([current_nonterminal, non_recursive_rules])
            
        else:
            raise Exception("UnstoppableLeftRecursion", "Unstoppable left recursion -> {} caused it".format(rule_pack))
            
        new_letter_num = new_letter_num + 1
        
    return new_rules

def ParseRule(rule, divider = " "):
    rule_list = rule.split(divider)
    return rule_list

def AddFactorization(unfixed_rules, new_letter):
    NEW_LETTER_START = new_letter
    new_rules = []
    new_letter_num = 1
    
    copy_of_old_rules = UniformRules(unfixed_rules)
    
    # узнать какую букву следует заюзать в этот раз
    for i in copy_of_old_rules:
        current_nonterminal = i[0]
        if i[0].startswith(current_nonterminal + "_" + NEW_LETTER_START):
            new_letter_num = max(new_letter_num, int(i[0][len(current_nonterminal + "_" + NEW_LETTER_START):])+1)

    # берем из унифицированных правил (так проще)
    for rule_pack in copy_of_old_rules:
        current_nonterminal = rule_pack[0]
        
        while rule_pack[1] != []:
            
            simmilar_rules = []
            minimal_rule_chunk = ParseRule(rule_pack[1][0])
            for rule in rule_pack[1]:
                parsed_rule = ParseRule(rule)
                for i in range(min(len(minimal_rule_chunk), len(parsed_rule))):
                    if parsed_rule[i] != minimal_rule_chunk[i]:
                        if i != 0:
                            minimal_rule_chunk = [parsed_rule[j] for j in range(len(parsed_rule)) if j < i]
                        break
                    else:
                        if i == 0:
                            simmilar_rules.append(rule)
                        if i + 1 == min(len(minimal_rule_chunk), len(parsed_rule)):
                            minimal_rule_chunk = [parsed_rule[j] for j in range(len(parsed_rule)) if j < i + 1]
                        
            minimal_rule_chunk_string = " ".join(minimal_rule_chunk)

            if len(simmilar_rules) > 1:
                new_rules.append([current_nonterminal, [minimal_rule_chunk_string + " " + current_nonterminal + "_" + NEW_LETTER_START + str(new_letter_num)]])
                for rule in simmilar_rules:
                    new_rules.append([current_nonterminal + "_" + NEW_LETTER_START + str(new_letter_num), [rule.replace(minimal_rule_chunk_string, "", 1).replace(" ", "", 1) if rule.replace(minimal_rule_chunk_string, "", 1) != "" else "e"]])
                    rule_pack[1].remove(rule)
                    
                new_letter_num = new_letter_num + 1
                    
            else:
                new_rules.append([current_nonterminal, [simmilar_rules[0]]])
                rule_pack[1].remove(simmilar_rules[0])
            
    return new_rules

def AddGuides(rules):
    copy_of_rules = copy.deepcopy(rules)
    set_of_nonterminals = set([rule_pack[0] for rule_pack in rules])

    is_nonterms_left = True
    nonterminals_readyness = {i:1 for i in set_of_nonterminals} #0 not, 1 probably not, 2 probably yes, 3 absolutly YES 

    for rule_pack in copy_of_rules:
        rule_pack.append(set())

    while is_nonterms_left:
        is_nonterms_left = False

        #закрепляем результаты готовности направляющих для нетерминалов
        nonterminals_readyness = {i:(j if j == 1 or j == 3 else j+1) for (i, j) in nonterminals_readyness.items()} 

        #для каждого правила
        for rule_pack in copy_of_rules:

            rule_start = ParseRule(rule_pack[1][0])[0]
            current_nonterm = rule_pack[0]

            if nonterminals_readyness[current_nonterm] == 3: #если направляющие для правила готовы, то пропускаем обработку текущ правила
                continue

            #смотрим чем является направляющая для правила
            if rule_start != "e":
                # это не пустой символ
                if rule_start in set_of_nonterminals:
                    # у нас нетерминал
                    if nonterminals_readyness[rule_start] == 3:
                        #если нетерминал уже есть в списке готовых, записать их значения
                        for pack in copy_of_rules: 
                            if pack[0] == rule_start:
                                for symbol in pack[2]:
                                    rule_pack[2].add(symbol)
                        #написать что нетерминал готов, если другое правило его не переписало в неготовое состояние
                        if nonterminals_readyness[current_nonterm] != 0:
                            nonterminals_readyness[current_nonterm] = 2
                    else:
                        # у нас нетерминал еще не готов
                        nonterminals_readyness[current_nonterm] = 0
                        is_nonterms_left = True
                else:
                    # у нас терминал
                    rule_pack[2].add(rule_start)
                    if nonterminals_readyness[current_nonterm] != 0:
                        nonterminals_readyness[current_nonterm] = 2
            else: 
                # у нас пустой символ
                # список букв после которых идет нужная нам буква, например для A->e, это A, мы пойдем ее искать в других правилах
                letters_that_could_end_with_e = [current_nonterm]

                for looking_letter in letters_that_could_end_with_e:
                    #print("Идем по {} букве".format(looking_letter))
                    # идем искать букву во всех правилах которая следует после е
                    for pack in copy_of_rules:
                        parsed_rule = ParseRule(pack[1][0])
                        for pos in range(len(parsed_rule)):
                            # нашли
                            if parsed_rule[pos] == looking_letter:
                                if pos + 1 != len(parsed_rule):
                                    # оно оказалось не последним символом
                                    if parsed_rule[pos + 1] in set_of_nonterminals:
                                        # наш следующий символ оказалсся нетерминалом... пишем его данные, если они есть
                                        if nonterminals_readyness[parsed_rule[pos + 1]] == 3:
                                            for i in copy_of_rules: 
                                                if i[0] == parsed_rule[pos + 1]:
                                                    for symbol in i[2]:
                                                        rule_pack[2].add(symbol)
                                            if nonterminals_readyness[current_nonterm] != 0:
                                                nonterminals_readyness[current_nonterm] = 2
                                        else:
                                            # у нас нетерминал оказался неготовый... ждем...
                                            if parsed_rule[pos + 1] != current_nonterm:
                                                nonterminals_readyness[current_nonterm] = 0
                                            for i in copy_of_rules: 
                                                if i[0] == parsed_rule[pos + 1]:
                                                    for symbol in i[2]:
                                                        rule_pack[2].add(symbol)
                                    else:
                                        # у нас попался терминал
                                        rule_pack[2].add(parsed_rule[pos + 1])
                                        if nonterminals_readyness[current_nonterm] != 0:
                                            nonterminals_readyness[current_nonterm] = 2

                                elif not (pack[0] in letters_that_could_end_with_e):
                                    # оно оказалось последним символом, идем искать по другой букве
                                    letters_that_could_end_with_e.append(pack[0])
    
    return copy_of_rules

def CheckIsItLL(rules):

    alreadyTakenGuides = dict()
    for rule_pack in rules:
        for guide in rule_pack[2]:
            for other_rule_pack in rules:
                if rule_pack != other_rule_pack and rule_pack[0] == other_rule_pack[0]:
                    for other_guide in other_rule_pack[2]:
                        if guide == other_guide:
                            raise Exception("Not LL: \n\n {0} nonterm conflict on \n\n {1} \n {2} \n \n and \n \n {3} \n {4}".format(rule_pack[0], rule_pack[1], rule_pack[2], other_rule_pack[1], other_rule_pack[2]))
    
def CreateTable(rules):
    set_of_nonterminals = set([rule_pack[0] for rule_pack in rules])
    
    new_table = []
    num_of_column = 1
    
    new_table.append(["№", "Symbol", "Guide", "GoTo", "ERR", "Read", "Stack", "END"])
    for rule_pack in rules:
        new_table.append([num_of_column, rule_pack[0], rule_pack[2], None, True, "", "", ""])
        if new_table[-2][1] == new_table[-1][1]:
            new_table[-2][4] = "False"
        num_of_column = num_of_column + 1
        
    rows_of_left_part = num_of_column
        
    for rule_pack_num in range(len(rules)):
        
        rule_pack = rules[rule_pack_num]
        symbol_pack = rule_pack[1][0].split(" ")
        
        new_table[rule_pack_num + 1][3] = num_of_column
        
        for symbol_num in range(len(symbol_pack)):
            symbol = symbol_pack[symbol_num]
            
            where_to_go = ""
            if symbol in set_of_nonterminals:
                for i in range(len(new_table[0 : rows_of_left_part])):
                    if new_table[i][1] == symbol:
                        where_to_go = i
                        break
            elif symbol == "e":
                where_to_go = "NULL"
            else:
                if symbol_num == len(symbol_pack) - 1:
                    where_to_go = "NULL"
                else:
                    where_to_go = num_of_column + 1
                
            
            is_set_stack = True if (symbol_num != len(symbol_pack) - 1 and symbol in set_of_nonterminals) else ""
            
            if not symbol in set_of_nonterminals:
                what_guide = set([symbol])
            else:
                what_guide = set()
                #what_guide = set(", ".join(i[2]) for i in new_table[0: rows_of_left_part] if i[1] == symbol)
                for i in new_table[0: rows_of_left_part]:
                    if i[1] == symbol:
                        for guide in i[2]:
                            what_guide.add(guide)


            if what_guide == set("e"):
                what_guide = rule_pack[2]
            
            is_read_symbol = True if not symbol in set_of_nonterminals and symbol != "e" else ""
            is_end = True if symbol == "$" else ""
            
            new_table.append([num_of_column, symbol, what_guide, where_to_go, True, is_read_symbol , is_set_stack, is_end])
            
            num_of_column = num_of_column + 1
            
            
    return new_table

def SortRules(table):
    new_table = copy.deepcopy(table)

    old_rule = new_table[0]
    old_rule_pos = -1

    for rule_pack_num in range(len(new_table)):
        old_rule_pos = old_rule_pos + 1
        if old_rule[0] != new_table[rule_pack_num][0]:

            for other_pack_num in range(old_rule_pos, len(new_table)):
                if new_table[other_pack_num][0] == old_rule[0]:
                    new_table.insert(old_rule_pos, new_table[other_pack_num])
                    new_table.pop(other_pack_num + 1)
                    
            
        old_rule = new_table[rule_pack_num]

    return new_table

class Runner_cl:
    
    def __init__(self, first_instance, table, end_symbol):
        self.table = table
        self.current_pos = first_instance
        self.is_end = False
        self.pos_stack = [first_instance]

    def Run(self, new_letter, pos):
        read = False
        error = True

        while self.pos_stack != []:
            

            while self.current_pos != "NULL":
                our_line = self.table[self.current_pos]
                letter = our_line[1]
                guides = our_line[2]
                go_to = our_line[3]
                error = our_line[4]
                read = our_line[5]
                stack = our_line[6]
                end = our_line[7]

                if new_letter in guides:
                    
                    if stack:
                        self.pos_stack.append(self.current_pos + 1)

                    self.is_end = True if end else False

                    self.current_pos = go_to

                    #print("We are now at {} position".format(self.current_pos))

                    if read:
                        return(self.pos_stack == [1] and self.is_end)

                elif error == "False": #ERR?
                    self.current_pos = self.current_pos + 1
                    #print("Jump when dealed with errors, to {} position".format(self.current_pos))
                
                else:
                    #print("There are trouble happen, '{}' letter was given, when '{}' were only possible at {}".format(new_letter, guides, pos))
                    raise Exception("UnexpectedSymbol", "'{}' letter was given, when '{}' were only possible at {}".format(new_letter, guides, pos))
                    #exit(0)

            if self.current_pos == "NULL":
                self.current_pos = self.pos_stack.pop()



def Run(rules, lr_letter, ft_letter, word = "", show_all = False):

    if show_all: 
        Print_2D_Table(UniformRules(rules))
    
    removed_lr_rules = RemoveLeftRecursion(rules, lr_letter)
    if show_all: 
        Print_2D_Table(removed_lr_rules)
    
    new_factorization = AddFactorization(removed_lr_rules, ft_letter)
    for i in range(5):
        new_factorization = AddFactorization(new_factorization, ft_letter)
    if show_all: 
        Print_2D_Table(new_factorization)
    
    guides_added = AddGuides(new_factorization)
    if show_all: 
        Print_2D_Table(guides_added)

    CheckIsItLL(guides_added)

    sorted_table = SortRules(guides_added)
    if show_all: 
        Print_2D_Table(sorted_table)

    ready_table = CreateTable(sorted_table)

    Print_2D_Table(ready_table, "[]'")

    return ready_table