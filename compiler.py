# Parsa Hosseini 98109583
# Mahdi Salmani 98105824
# We designed our Scanner based on dfa.png

SYMBOL = [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '<']
WHITESPACE = [' ', '\r', '\t', '\v', '\f']
EOF = ''
DFA = {  # 0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17  18  19
    'letter': [1, 1, 0, -2, 0, 0, 0, 9, 0, 0, 11, 0, -5, 13, 13, 0, 16],
    'digit': [3, 1, 0, 3, 0, 0, 0, 9, 0, 0, 11, 0, -5, 13, 13, 0, 16],
    'symbol': [6, 2, 0, 4, 0, 0, 0, 9, 0, 0, 11, 0, -5, 13, 13, 0, 16],
    'whitespace': [5, 2, 0, 4, 0, 0, 0, 9, 0, 0, 11, 0, -5, 13, 13, 0, 16],
    '\n': [5, 2, 0, 4, 0, 0, 0, 9, 0, 0, 11, 0, -5, 13, 13, 0, 15],
    '/': [12, 2, 0, 4, 0, 0, 0, 9, 0, 0, -3, 0, 16, 13, 15, 0, 16],
    '=': [7, 2, 0, 4, 0, 0, 0, 8, 0, 0, 11, 0, -5, 13, 13, 0, 16],
    '*': [10, 2, 0, 4, 0, 0, 0, 9, 0, 0, 11, 0, 13, 14, 14, 0, 16],
    EOF: [5, 2, 0, 4, 0, 0, 0, 9, 0, 0, 11, 0, -5, -4, -4, 0, 15],
    'invalid': [-1, -1, 0, -2, 0, 0, 0, -1, 0, 0, -1, 0, -1, 13, 13, 0, 16]
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


tokens = {}
errors = {}


def add_token(lineno, token):
    if lineno in tokens:
        tokens[lineno].append(token)
    else:
        tokens[lineno] = [token]


def add_error(lineno, error):
    if lineno in errors:
        errors[lineno].append(error)
    else:
        errors[lineno] = [error]


SYMBOL_TABLE = ['if', 'else', 'void', 'int', 'repeat', 'break', 'until', 'return']
NO_KEYWORDS = len(SYMBOL_TABLE)


def get_token(state, lexeme):
    if state == 2:
        if lexeme in SYMBOL_TABLE and SYMBOL_TABLE.index(lexeme) < NO_KEYWORDS:
            return 'KEYWORD', lexeme
        else:
            if lexeme not in SYMBOL_TABLE:
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


f = open('input.txt', 'rb')

lineno = 1
while True:
    state = 0  # Start state
    temp_lineno = lineno
    raw_token = ''
    character = True
    while character:
        character = f.read(1).decode('utf-8')

        state = transit(state, character)
        if state in LOOK_AHEAD_STATES:
            f.seek(f.tell() - 1, 0)
        else:
            if character == '\n':
                temp_lineno += 1
            raw_token += character
        if state in GOAL_STATES:
            token = get_token(state, raw_token)
            if token is not None:
                add_token(lineno, token)
            lineno = temp_lineno  ## ?????
            break
        if state < 0:
            error = get_error(state, raw_token)
            add_error(lineno, error)
            lineno = temp_lineno  ## ?????
            break
    if not character:
        break
f.close()

f = open('symbol_table.txt', 'w')
for i in range(1, len(SYMBOL_TABLE) + 1):
    f.write(f'{i}.\t{SYMBOL_TABLE[i - 1]}\n')
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
