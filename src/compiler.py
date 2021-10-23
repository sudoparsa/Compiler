SYMBOL = [';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '=', '<']
WHITESPACE = [' ', '\n', '\r', '\t', '\v', '\f']
EOF = ''


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
tokens = {}
errors = {}


def add_token(lineno, token):
    if lineno in tokens:
        tokens[lineno].append(token)
    else:
        tokens[lineno] = [token]


def add_errors(lineno, error):
    if lineno in errors:
        errors[lineno].append(error)
    else:
        errors[lineno] = [error]


SYMBOL_TABLE = ['', 'if', 'else', 'void', 'int', 'repeat', 'break', 'until', 'return']
input = """int count;
int result[50];


int f(int a, int result[#]) {
    count =## count + 1;
    if(result[a - 1]){
        return result[a - 1];
    } else {
        if (a == 1) {
            result[a - 1] = 1;
            return 1;
        } else if (a ===== 2){
            result[a - 1] = 1;
            return 1;
        } else {
            result[a - 1] = f(a - 2, result) + f(a - 1, result);
            return result[a - 1];
        }
    }
}

void main(void$) {
    int i;
    i = 0;
    repeat {
        result[i] = 0;
        i = i *## 2;
    } until (50 < i)
    count = 0;
    output(f(40, result));
    output(count);
}
1941"""

cursor = 0
lineno = 1
while cursor < len(input):
    temp = cursor
    s1, s2, s3, s4, s5 = 0, 0, 0, 0, 0
    s1_goal, s2_goal, s3_goal, s4_goal, s5_goal = False, False, False, False, False
    invalid_number, unclosed_comment, unmatched_comment, look_ahead = False, False, False, False
    temp_lineno = lineno
    while temp <= len(input):

        if temp == len(input):
            character = EOF
        else:
            character = input[temp]

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
            cursor = temp + 1
            break

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
            break

        temp += 1

print(SYMBOL_TABLE)
print()
print(errors)
print()
for line in tokens:
    print(line, tokens[line])
