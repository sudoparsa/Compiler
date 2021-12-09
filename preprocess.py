terminals = ['$', 'ID', ';', '[', 'NUM', ']', '(', ')', 'int', 'void', ',', '{', '}', 'break', 'if', 'endif', 'else',
             'repeat', 'until', 'return', '=', '<', '==', '+', '-', '*']

nterminals = ['Program', 'Declaration-list', 'Declaration', 'Declaration-initial', 'Declaration-prime',
              'Var-declaration-prime', 'Fun-declaration-prime', 'Type-specifier', 'Params', 'Param-list', 'Param',
              'Param-prime', 'Compound-stmt', 'Statement-list', 'Statement', 'Expression-stmt', 'Selection-stmt',
              'Else-stmt', 'Iteration-stmt', 'Return-stmt', 'Return-stmt-prime', 'Expression', 'B', 'H',
              'Simple-expression-zegond', 'Simple-expression-prime', 'C', 'Relop', 'Additive-expression',
              'Additive-expression-prime', 'Additive-expression-zegond', 'D', 'Addop', 'Term', 'Term-prime',
              'Term-zegond', 'G', 'Factor', 'Var-call-prime', 'Var-prime', 'Factor-prime', 'Factor-zegond', 'Args',
              'Arg-list', 'Arg-list-prime']

first = {'Program': ['$', 'int', 'void'], 'Declaration-list': ['int', 'void', 'EPSILON'],
         'Declaration': ['int', 'void'], 'Declaration-initial': ['int', 'void'], 'Declaration-prime': [';', '[', '('],
         'Var-declaration-prime': [';', '['], 'Fun-declaration-prime': ['('], 'Type-specifier': ['int', 'void'],
         'Params': ['int', 'void'], 'Param-list': [',', 'EPSILON'], 'Param': ['int', 'void'],
         'Param-prime': ['[', 'EPSILON'], 'Compound-stmt': ['{'],
         'Statement-list': ['ID', ';', 'NUM', '(', '{', 'break', 'if', 'repeat', 'return', 'EPSILON'],
         'Statement': ['ID', ';', 'NUM', '(', '{', 'break', 'if', 'repeat', 'return'],
         'Expression-stmt': ['ID', ';', 'NUM', '(', 'break'], 'Selection-stmt': ['if'], 'Else-stmt': ['endif', 'else'],
         'Iteration-stmt': ['repeat'], 'Return-stmt': ['return'], 'Return-stmt-prime': ['ID', ';', 'NUM', '('],
         'Expression': ['ID', 'NUM', '('], 'B': ['[', '(', '=', '<', '==', '+', '-', '*', 'EPSILON'],
         'H': ['=', '<', '==', '+', '-', '*', 'EPSILON'], 'Simple-expression-zegond': ['NUM', '('],
         'Simple-expression-prime': ['(', '<', '==', '+', '-', '*', 'EPSILON'], 'C': ['<', '==', 'EPSILON'],
         'Relop': ['<', '=='], 'Additive-expression': ['ID', 'NUM', '('],
         'Additive-expression-prime': ['(', '+', '-', '*', 'EPSILON'], 'Additive-expression-zegond': ['NUM', '('],
         'D': ['+', '-', 'EPSILON'], 'Addop': ['+', '-'], 'Term': ['ID', 'NUM', '('],
         'Term-prime': ['(', '*', 'EPSILON'], 'Term-zegond': ['NUM', '('], 'G': ['*', 'EPSILON'],
         'Factor': ['ID', 'NUM', '('], 'Var-call-prime': ['[', '(', 'EPSILON'], 'Var-prime': ['[', 'EPSILON'],
         'Factor-prime': ['(', 'EPSILON'], 'Factor-zegond': ['NUM', '('], 'Args': ['ID', 'NUM', '(', 'EPSILON'],
         'Arg-list': ['ID', 'NUM', '('], 'Arg-list-prime': [',', 'EPSILON']}

follow = {'Program': [''],
          'Declaration-list': ['$', 'ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'repeat', 'return'],
          'Declaration': ['$', 'ID', ';', 'NUM', '(', 'int', 'void', '{', '}', 'break', 'if', 'repeat', 'return'],
          'Declaration-initial': [';', '[', '(', ')', ','],
          'Declaration-prime': ['$', 'ID', ';', 'NUM', '(', 'int', 'void', '{', '}', 'break', 'if', 'repeat', 'return'],
          'Var-declaration-prime': ['$', 'ID', ';', 'NUM', '(', 'int', 'void', '{', '}', 'break', 'if', 'repeat',
                                    'return'],
          'Fun-declaration-prime': ['$', 'ID', ';', 'NUM', '(', 'int', 'void', '{', '}', 'break', 'if', 'repeat',
                                    'return'], 'Type-specifier': ['ID'], 'Params': [')'], 'Param-list': [')'],
          'Param': [')', ','], 'Param-prime': [')', ','],
          'Compound-stmt': ['$', 'ID', ';', 'NUM', '(', 'int', 'void', '{', '}', 'break', 'if', 'endif', 'else',
                            'repeat', 'until', 'return'], 'Statement-list': ['}'],
          'Statement': ['ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'endif', 'else', 'repeat', 'until', 'return'],
          'Expression-stmt': ['ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'endif', 'else', 'repeat', 'until',
                              'return'],
          'Selection-stmt': ['ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'endif', 'else', 'repeat', 'until',
                             'return'],
          'Else-stmt': ['ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'endif', 'else', 'repeat', 'until', 'return'],
          'Iteration-stmt': ['ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'endif', 'else', 'repeat', 'until',
                             'return'],
          'Return-stmt': ['ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'endif', 'else', 'repeat', 'until', 'return'],
          'Return-stmt-prime': ['ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'endif', 'else', 'repeat', 'until',
                                'return'], 'Expression': [';', ']', ')', ','], 'B': [';', ']', ')', ','],
          'H': [';', ']', ')', ','], 'Simple-expression-zegond': [';', ']', ')', ','],
          'Simple-expression-prime': [';', ']', ')', ','], 'C': [';', ']', ')', ','], 'Relop': ['ID', 'NUM', '('],
          'Additive-expression': [';', ']', ')', ','], 'Additive-expression-prime': [';', ']', ')', ',', '<', '=='],
          'Additive-expression-zegond': [';', ']', ')', ',', '<', '=='], 'D': [';', ']', ')', ',', '<', '=='],
          'Addop': ['ID', 'NUM', '('], 'Term': [';', ']', ')', ',', '<', '==', '+', '-'],
          'Term-prime': [';', ']', ')', ',', '<', '==', '+', '-'],
          'Term-zegond': [';', ']', ')', ',', '<', '==', '+', '-'], 'G': [';', ']', ')', ',', '<', '==', '+', '-'],
          'Factor': [';', ']', ')', ',', '<', '==', '+', '-', '*'],
          'Var-call-prime': [';', ']', ')', ',', '<', '==', '+', '-', '*'],
          'Var-prime': [';', ']', ')', ',', '<', '==', '+', '-', '*'],
          'Factor-prime': [';', ']', ')', ',', '<', '==', '+', '-', '*'],
          'Factor-zegond': [';', ']', ')', ',', '<', '==', '+', '-', '*'], 'Args': [')'], 'Arg-list': [')'],
          'Arg-list-prime': [')']}

first_epsilon = []
for nterminal in nterminals:
    if 'EPSILON' in first[nterminal]:
        first_epsilon.append(nterminal)


def extract_all_productions(production):
    all = []
    start = 0
    for i in range(len(production)):
        if production[i] == '|':
            all.append(production[start: i])
            start = i + 1
    all.append(production[start: len(production)])
    return all


def get_productions(file):
    productions = {}
    for line in file:
        production = line.split()
        production.remove('->')
        productions[production[0]] = extract_all_productions(production[1:])
    return productions


def get_dfa(file):
    productions = get_productions(file)
    dfa = {}
    for nt, pros in productions.items():
        goal_state = len(pros[0])
        table = {}
        index = 0
        for pro in pros:
            state = 0
            for i in range(len(pro)):
                token = pro[i]
                if state not in table:
                    table[state] = {}
                if state != 0:
                    next_state = state + 1
                else:
                    next_state = state + index + 1
                if i == len(pro) - 1:
                    next_state = goal_state
                table[state][token] = next_state
                if next_state > state:
                    index += 1
                state = next_state
        dfa[nt] = table
    return dfa


'''print(productions)
print(dfa)
print(sum([len(dfa[key].keys()) + 1 for key in dfa.keys()]))
print(sum([sum(len(c)-1 for c in v)+2 for k,v in productions.items()]))'''


def get_action_table(file_path='c-minus_001.txt'):
    file = open(file_path, 'r')
    dfa = get_dfa(file)
    print(dfa)
    action_table = {}
    for nt, graph in dfa.items():
        for state, adjacent in graph.items():
            for t in terminals:
                for token, next_state in adjacent.items():
                    if t == token:
                        action_table[(nt, state, t)] = f'goto {next_state}'
                    elif token in nterminals and t in first[token]:
                        action_table[(nt, state, t)] = f'call {token} {next_state}'
                    elif token in first_epsilon and t in follow[token]:
                        action_table[(nt, state, t)] = f'call {token} {next_state}'
                if (nt, state, t) in action_table.keys():
                    continue
                for token, next_state in adjacent.items():
                    if token in nterminals and (token not in first_epsilon) and t in follow[token]:
                        action_table[(nt, state, t)] = f'missing {token} {next_state}'
                if (nt, state, t) in action_table.keys():
                    continue

                token, next_state = list(adjacent.items())[0]
                if token in terminals:
                    action_table[(nt, state, t)] = f'missing {token} {next_state}'
                else:
                    action_table[(nt, state, t)] = f'illegal {t} {next_state}'
    file.close()
    return action_table


if __name__ == '__main__':
    action_table = get_action_table()
    #print(action_table)
