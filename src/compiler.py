SYMBOL = [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '<']
WHITESPACE = [' ', '\r', '\t', '\v', '\f']
EOF = ''
<<<<<<< HEAD:compiler.py
DFA = {            #0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17  18  19
    'letter':       [1,     1,0,    -2,0,0,0,   9,0,0,  11,0,   -5, 13, 13,0,   16],
    'digit':        [3,     1,0,    3,0,0,0,    9,0,0,  11,0,   -5, 13, 13,0,   16],
    'symbol':       [6,     2,0,    4,0,0,0,    9,0,0,  11,0,   -5, 13, 13,0,   16],
    'whitespace':   [5,     2,0,    4,0,0,0,    9,0,0,  11,0,   -5, 13, 13,0,   16],
    '\n':           [5,     2,0,    4,0,0,0,    9,0,0,  11,0,   -5, 13, 13,0,   15],
    '/':            [12,    2,0,    4,0,0,0,    9,0,0,  -3,0,   16, 13, 15,0,   16],
    '=':            [7,     2,0,    4,0,0,0,    8,0,0,  11,0,   -5, 13, 13,0,   16],
    '*':            [10,    2,0,    4,0,0,0,    9,0,0,  11,0,   13, 14, 14,0,   16],
    EOF:            [5,     2,0,    4,0,0,0,    9,0,0,  11,0,   -5, -4, -4,0,   15],
    'invalid':      [-1,    -1,0,   -2,0,0,0,   -1,0,0, -1,0,   -1, 13, 13,0,   16]
}
GOAL_STATES = [2, 4, 5, 6, 8, 9, 11, 15]
LOOK_AHEAD_STATES = [2, 4, 9, 11, -5]

def transit(current_state, character):
    if character.isalpha():
        next_state = DFA['letter'][current_state]
    elif character.isdigit():
        next_state = DFA['digit'][current_state]
    elif character in WHITESPACE:
        next_state = DFA['whitespace'][current_state]
    elif character in SYMBOL:
        next_state = DFA['symbol'][current_state]
    elif character in ['/', '=', '*', EOF, '\n']:
        next_state = DFA[character][current_state]
    else:
        next_state = DFA['invalid'][current_state]
    
    return next_state

=======


def isDigit(character):
    return character.isdigit()


def isLetter(character):
    return character.isalpha()


def isSymbol(character, count_equal=True, count_star=True):
    if character == '*':
        if count_star:
            return True
        else:
            return False
    if character == '=':
        if count_equal:
            return True
        else:
            return False
    else:
        return character in SYMBOL


####    Identifier DFA  ####
ID_DFA = {
    'letter': [1, 1, 2],
    'digit': [-1, 1, 2],
    'other': [-1, 2, 2]
}


def transit_ID(current_state, character):
    def isOther(character):
        if character in WHITESPACE or character in SYMBOL or character in ['/', '//', EOF]:
            return True
        return False

    if isLetter(character):
        next_state = ID_DFA['letter'][current_state]
    elif isDigit(character):
        next_state = ID_DFA['digit'][current_state]
    elif isOther(character):
        next_state = ID_DFA['other'][current_state]
    else:
        next_state = -1

    is_goal = next_state == 2

    return next_state, is_goal


####    Number DFA      ####
NUM_DFA = {
    'digit': [1, 1, 2],
    'other': [-1, 2, 2]
}


def transit_NUM(current_state, character):
    def isOther(character):
        if character in WHITESPACE or character in SYMBOL or character in ['/', EOF]:
            return True
        return False

    if isDigit(character):
        next_state = NUM_DFA['digit'][current_state]
    elif isOther(character):
        next_state = NUM_DFA['other'][current_state]
    else:
        next_state = -1

    invalid_number = isLetter(character) and current_state == 1
    is_goal = next_state == 2

    return next_state, is_goal, invalid_number


####    WhiteSpace DFA  ####
WHITESPACE_DFA = {
    'whitespace': [1, 1]
}


def transit_WhiteSpace(current_state, character):
    if character in WHITESPACE:
        next_state = WHITESPACE_DFA['whitespace'][current_state]
    else:
        next_state = -1

    is_goal = next_state == 1

    return next_state, is_goal


####    Symbol DFA      ####
SYMBOL_DFA = {
    'symbol-': [1, 1, 4, 3, 4, 6, 6],
    '=': [2, 1, 3, 3, 4, 6, 6],
    '*': [5, 1, 4, 3, 4, 6, 6],
    'other': [-1, 1, 4, 3, 4, 6, 6]
}


def transit_Symbol(current_state, character):
    def isOther(character):
        if character in WHITESPACE or character in [EOF, '/'] or isLetter(character) or isDigit(character):
            return True
        return False

    if current_state == 5 and character == '/':
        next_state = -1
    elif isOther(character):
        next_state = SYMBOL_DFA['other'][current_state]
    elif character in ['=', '*']:
        next_state = SYMBOL_DFA[character][current_state]
    elif isSymbol(character, count_equal=False, count_star=False):
        next_state = SYMBOL_DFA['symbol-'][current_state]
    else:
        next_state = -1

    is_goal = next_state in [1, 3, 4, 6]
    unmatched_comment = character == '/' and current_state == 5
    look_ahead = next_state == 4 or current_state == 5  #####????????

    return next_state, is_goal, unmatched_comment, look_ahead


# current_state = 0
# for x in "@":
#     next_state, is_goal, unmatched_comment, look_ahead = transit_Symbol(current_state, x)
#     print(next_state, is_goal, unmatched_comment, look_ahead)
#     current_state = next_state

#### COMMENT DFA        ####
COMMENT_DFA = {
    '/': [1, 3, 2, 3, 5, 5],
    '*': [-1, 2, 4, 3, 4, 5],
    '\n': [-1, -1, 2, 5, 2, 5],
    EOF: [-1, -1, -1, 5, -1, 5],  ###END OF FILE
    'other': [-1, -1, 2, 3, 2, 5]
}


def transit_COMMENT(current_state, character):
    def isOther(character):
        return not (character == EOF or character == '*' or character == '\n' or character == '/')

    if isOther(character):
        next_state = COMMENT_DFA['other'][current_state]
    elif character in [EOF, '\n', '/', '*']:
        next_state = COMMENT_DFA[character][current_state]
    else:
        next_state = -1

    is_goal = next_state == 5
    unclosed_comment = character == EOF and current_state in [2, 4]

    return next_state, is_goal, unclosed_comment


global tokens, errors
>>>>>>> e6cb723a8f80609535632e49b47ea74d8159fec3:src/compiler.py
tokens = {}
errors = {}


def add_token(lineno, token):
    if lineno in tokens:
        tokens[lineno].append(token)
    else:
        tokens[lineno] = [token]
<<<<<<< HEAD:compiler.py
def add_error(lineno, error):
=======


def add_errors(lineno, error):
>>>>>>> e6cb723a8f80609535632e49b47ea74d8159fec3:src/compiler.py
    if lineno in errors:
        errors[lineno].append(error)
    else:
        errors[lineno] = [error]


SYMBOL_TABLE = ['', 'if', 'else', 'void', 'int', 'repeat', 'break', 'until', 'return']
def get_token(state, lexeme):
    if state == 2:
        if lexeme in SYMBOL_TABLE and SYMBOL_TABLE.index(lexeme) <= 8:
                return 'KEYWORD', lexeme
        else:
            if not lexeme in SYMBOL_TABLE:
                    SYMBOL_TABLE.append(lexeme)
            return 'ID', lexeme
    if state == 4:
        return 'NUM', lexeme
    if state == 5:
        return None
    if state == 6 or state == 8 or state == 9 or state == 11:
        return 'SYMBOL', lexeme
    if state == 15:
        return None 

def get_error(state, lexeme):
    if state == -1 or state == -5:
        return lexeme, 'Invalid input'
    if state == -2:
        return lexeme, 'Invalid number'
    if state == -3:
        return lexeme, 'Unmatched comment'
    if state == -4:
        return lexeme[:min([7, len(lexeme)])] + '...', 'Unclosed comment'


f = open('input.txt', 'r')
inp = f.read()
f.close()

cursor = 0
lineno = 1
while cursor < len(inp):
    temp = cursor
    state = 0
    temp_lineno = lineno
<<<<<<< HEAD:compiler.py
    while temp <= len(inp):
        
        if temp == len(inp):
=======
    while temp <= len(input):

        if temp == len(input):
>>>>>>> e6cb723a8f80609535632e49b47ea74d8159fec3:src/compiler.py
            character = EOF
        else:
            character = inp[temp]

<<<<<<< HEAD:compiler.py

        state = transit(state, character)
        if state in LOOK_AHEAD_STATES:
            temp -= 1
        else:
            if character == '\n':
                temp_lineno += 1
        if state in GOAL_STATES:
            token = get_token(state, inp[cursor:temp + 1])
            if not token == None:
                add_token(lineno, token)
=======
        if character == '\n':
            temp_lineno += 1
        if not s1 == -1:
            s1, s1_goal = transit_ID(s1, character)
        if not s2 == -1:
            s2, s2_goal, invalid_number = transit_NUM(s2, character)
        if not s3 == -1:
            s3, s3_goal = transit_WhiteSpace(s3, character)
        if not s4 == -1:
            s4, s4_goal, unmatched_comment, look_ahead = transit_Symbol(s4, character)
        if not s5 == -1:
            s5, s5_goal, unclosed_comment = transit_COMMENT(s5, character)

        # print(s1, s2, s3, s4, s5)
        if s1_goal:
            if input[cursor:temp] in SYMBOL_TABLE and SYMBOL_TABLE.index(input[cursor:temp]) <= 8:
                # print(lineno, ('KEYWORD', input[cursor:temp]))
                add_token(lineno, ('KEYWORD', input[cursor:temp]))
            else:
                if not input[cursor:temp] in SYMBOL_TABLE:
                    SYMBOL_TABLE.append(input[cursor:temp])
                # print(lineno, ('ID', input[cursor:temp]))
                add_token(lineno, ('ID', input[cursor:temp]))
            cursor = temp
            lineno = temp_lineno
            break
        if s2_goal:
            # print(lineno, ('NUM', input[cursor:temp]))
            add_token(lineno, ('NUM', input[cursor:temp]))
            lineno = temp_lineno
            cursor = temp
            break
        if s3_goal:
            cursor += 1
            lineno = temp_lineno
            break
        if s4_goal:
            if look_ahead:
                # print(lineno, ('SYMBOL', input[cursor:temp]))
                add_token(lineno, ('SYMBOL', input[cursor:temp]))
                cursor = temp
            else:
                # print(lineno, ('SYMBOL', input[cursor:temp + 1]))
                add_token(lineno, ('SYMBOL', input[cursor:temp + 1]))
                cursor = temp + 1
            lineno = temp_lineno
            break
        if s5_goal:
            # print(input[cursor:temp + 1])
            lineno = temp_lineno
>>>>>>> e6cb723a8f80609535632e49b47ea74d8159fec3:src/compiler.py
            cursor = temp + 1
            lineno = temp_lineno ## ?????
            break
<<<<<<< HEAD:compiler.py
        if state < 0:
            error = get_error(state, inp[cursor:temp + 1])
            add_error(lineno, error) 
            cursor = temp + 1
            lineno = temp_lineno ## ?????
=======

        if s1 == -1 and s2 == -1 and s3 == -1 and s4 == -1 and s5 == -1:
            lineno = temp_lineno
            if invalid_number:
                # print(lineno, (input[cursor:temp + 1], 'Invalid number'))
                add_errors(lineno, (input[cursor:temp + 1], 'Invalid number'))
                cursor = temp + 1
            elif unclosed_comment:
                # print(lineno, (input[cursor:temp], 'Unclosed comment'))
                add_errors(lineno, (input[cursor:temp + 1], 'Unclosed comment'))
                cursor = temp
            elif unmatched_comment:
                # print(lineno,('*/', 'Unmatched comment'))
                add_errors(lineno, ('*/', 'Unmatched comment'))
                cursor = temp + 1
            else:
                # print(lineno, (input[cursor:temp + 1], 'Invalid Input'))
                add_errors(lineno, (input[cursor:temp + 1], 'Invalid Input'))
                cursor = temp + 1
>>>>>>> e6cb723a8f80609535632e49b47ea74d8159fec3:src/compiler.py
            break
        temp += 1

<<<<<<< HEAD:compiler.py
f = open('symbol_table.txt', 'w')
for i in range(1, len(SYMBOL_TABLE)):
    f.write(f'{i}.\t{SYMBOL_TABLE[i]}\n')
f.close()

f = open('tokens.txt', 'w')
for key in tokens:
    f.write(f'{key}.\t')
    for token in tokens[key]:
        f.write(f'({token[0]}, {token[1]}) ')
    f.write('\n')
f.close()

f = open('lexical_errors.txt', 'w')
if not errors:
    f.write('There is no lexical error.')
else:
    for key in errors:
        f.write(f'{key}.\t')
        for token in errors[key]:
            f.write(f'({token[0]}, {token[1]}) ')
        f.write('\n')
f.close()


=======
print(SYMBOL_TABLE)
print()
print(errors)
print()
for line in tokens:
    print(line, tokens[line])
>>>>>>> e6cb723a8f80609535632e49b47ea74d8159fec3:src/compiler.py
