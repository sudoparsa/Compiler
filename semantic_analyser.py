from preprocess import get_action_symbols
from SymbolTable import *
import code_gen

params_type_list = []
last_action = ''
last_lexeme = ''


def check_scope(token, lineno):
    if get_table_address(token)[1] != 'error':
        return False, ''
    return True, f"#{lineno} : Semantic Error! '{token}' is not defined."


def add_param(last_action):
    global params_type_list
    if last_action == '#push_id' and get_type(last_lexeme) == 'arr':
        params_type_list.append('arr')
        return
    params_type_list.append('var')


def check_void(action, lineno):
    ss = code_gen.get_semantic_stack()
    if action == '#declare_id':
        lexeme = ss[-1]
        type = ss[-2]
    else:
        lexeme = ss[-2]
        type = ss[-3]
    if type != 'void':
        return False, ''
    return True, f"#{lineno} : Semantic Error! Illegal type of void for '{lexeme}'."


def check_args(lineno):
    global params_type_list
    ss = code_gen.get_semantic_stack()
    index = -1
    while ss[index] == ['param']:
        index -= 2
    lexeme = ss[index]
    if lexeme == 'output':
        params_type_list = []
        return False, ''
    args = get_func_args(lexeme)
    if len(args) == len(params_type_list):
        return check_parameter_type_matching(lineno, args, lexeme)
    params_type_list = []
    return True, f"#{lineno} : Semantic Error! Mismatch in numbers of arguments of '{lexeme}'."


def check_parameter_type_matching(lineno, args, lexeme):
    global params_type_list
    message = ''
    flag = False
    index = 1
    for arg, param in zip(args, params_type_list):
        if arg == 'var' and param == 'arr':
            flag = True
            message += f"#{lineno} : Semantic Error! Mismatch in type of argument {index} of '{lexeme}'. Expected 'int' but got 'array' instead.\n"
        if arg == 'arr' and param == 'var':
            flag = True
            message += f"#{lineno} : Semantic Error! Mismatch in type of argument {index} of '{lexeme}'. Expected 'array' but got 'int' instead.\n"
        index += 1
    params_type_list = []
    return flag, message[:len(message) - 1]


def check_type_mismatch(lineno):
    lexeme = code_gen.get_semantic_stack()[-1]
    if get_type(lexeme) == 'arr':
        return True, f"#{lineno} : Semantic Error! Type mismatch in operands, Got array instead of int."
    return False, ''


def check_break(lineno):
    repeat_no = code_gen.repeat_no
    if repeat_no > 0:
        return False, ''
    return True, f"#{lineno - 1} : Semantic Error! No 'repeat ... until' found for 'break'."


# Returns True when there is semantic error.
def semantic_checks(st, nt, token, state, next_state, lineno):
    global last_action
    action_symbols = get_action_symbols()
    if st == 'return':
        next_state = state
    if (state, next_state) in action_symbols[nt]:
        for action in action_symbols[nt][(state, next_state)]:
            if (nt == 'Expression' or nt == 'Factor') and action == '#push_token':
                last_action = action
                return check_scope(token, lineno)
            if action == '#declare_id' or action == '#declare_arr':
                last_action = action
                return check_void(action, lineno)
            if action == '#call':
                last_action = action
                return check_args(lineno)
            if action == '#break_until':
                last_action = action
                return check_break(lineno)
            if nt != 'Factor-prime' and action == '#push_id':
                last_action = action
                return check_type_mismatch(lineno)
            if nt == 'Factor-prime' and action == '#push_id':
                global last_lexeme
                last_lexeme = code_gen.semantic_stack[-1]
            if action == '#push_param':
                add_param(last_action)
            last_action = action

    return False, ''
