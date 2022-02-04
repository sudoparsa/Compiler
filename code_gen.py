from SymbolTable import *
from preprocess import get_action_symbols

rv_register = 450
dp_register = 454
gp_register = 458
ap_register = 462

program_block = [
    f'(ASSIGN, #0, {rv_register}, )',
    f'(ASSIGN, #500, {dp_register}, )',
    f'(ASSIGN, #15000, {gp_register}, )',
    f'(ASSIGN, #20000, {ap_register}, )',
    f'(JP, 11, , )',
    f'(ADD, #4, {dp_register}, 3000)',
    f'(ADD, #8, {dp_register}, 3008)',
    f'(PRINT, @3008, , )',
    f'(ASSIGN, @{dp_register}, {dp_register}, )',
    f'(ASSIGN, @3000, 3004, )',
    f'(JP, @3004, , )'
]

temp_pointer = 3012

semantic_stack = []

break_list = []

declare_main = False


def get_semantic_stack():
    return semantic_stack


def add_symbol_id(lexeme, type, scope, func=False, func_address=0, arr=False):
    add_to_symbol_table(lexeme, type, scope, func, func_address, arr)


def get_address(lexeme):
    return get_table_address(lexeme)


def get_free_address():
    return get_table_free_address()


def reset_scope():
    table_reset_scope()


output_mode = False
scope = 'G'
add_symbol_id('output', 'void', 'G', func=True, func_address=5)

args_type = []
func_lexeme = ''
repeat_no = 0


def get_temp():
    global temp_pointer
    temp_pointer += 4
    return temp_pointer - 4


def push_token(token):
    semantic_stack.append(token)


def set_args(token):
    global args_type
    set_func_args(func_lexeme, args_type)
    args_type = []


def set_arr(token):
    set_table_arr(semantic_stack.pop())


def declare_id(token, arg=False):
    lexeme = semantic_stack.pop()
    type = semantic_stack.pop()
    add_symbol_id(lexeme, type, scope)

    if arg:
        semantic_stack.append(lexeme)
    else:
        temp = get_temp()
        local_address, _scope = get_address(lexeme)
        if scope == 'G':
            program_block.append(f'(ADD, {gp_register}, #{local_address}, {temp})')
        else:
            program_block.append(f'(ADD, {dp_register}, #{local_address + 8}, {temp})')
        program_block.append(f'(ASSIGN, #0, @{temp}, )')


def declare_arg(token):
    global args_type
    args_type.append(semantic_stack[-1])
    declare_id(token, True)


def push_num(token):
    semantic_stack.append(f'#{token}')


def assign_array_memory(size):
    for i in range(size):
        program_block.append(f'(ASSIGN, #0, @{ap_register}, )')
        program_block.append(f'(ADD, #4, {ap_register}, {ap_register})')


def declare_arr(token):
    size = semantic_stack.pop()
    length = int(size[1:])
    lexeme = semantic_stack.pop()
    type = semantic_stack.pop()
    add_symbol_id(lexeme, type, scope, arr=True)
    temp = get_temp()
    address, _scope = get_address(lexeme)

    if scope == 'G':
        program_block.append(f'(ADD, {gp_register}, #{address}, {temp})')
    else:
        program_block.append(f'(ADD, {dp_register}, #{address + 8}, {temp})')

    program_block.append(f'(ASSIGN, {ap_register}, @{temp}, )')

    assign_array_memory(length)


def new_scope(token):
    global scope
    scope = 'L'


def end_scope(token):
    global scope
    scope = 'G'
    reset_scope()


def jp(token):
    i = semantic_stack.pop()
    here = len(program_block)
    program_block[i] = f'(JP, {here}, , )'


def fill_jump(token):
    global declare_main
    if not declare_main:
        i = semantic_stack.pop()
        here = len(program_block)
        program_block[i] = f'(JP, {here}, , )'
    else:
        declare_main = False


def save(token):
    semantic_stack.append(len(program_block))
    program_block.append("")


def declare_func(token):
    lexeme = semantic_stack.pop()
    type = semantic_stack.pop()
    if lexeme == 'main':
        global declare_main
        declare_main = True
    else:
        save(token)
    here = len(program_block)
    add_symbol_id(lexeme, type, 'G', func=True, func_address=here)
    global func_lexeme
    func_lexeme = lexeme


def pop(token):
    semantic_stack.pop()


def break_until(token):
    break_list.append(len(program_block))
    program_block.append("")


def jpf(token):
    i = semantic_stack.pop()
    e = semantic_stack.pop()
    here = len(program_block)

    program_block[i] = f'(JPF, {e}, {here}, )'


def jpf_save(token):
    i = semantic_stack.pop()
    e = semantic_stack.pop()
    here = len(program_block)
    semantic_stack.append(here)

    program_block[i] = f'(JPF, {e}, {here + 1}, )'
    program_block.append('')


def label(token):
    here = len(program_block)
    semantic_stack.append(here)
    global repeat_no
    repeat_no += 1


def until(token):
    e = semantic_stack.pop()
    i = semantic_stack.pop()
    program_block.append(f'(JPF, {e}, {i}, )')


def handle_breaks(token):
    here = len(program_block)
    global break_list
    for br in break_list:
        program_block[br] = f'(JP, {here}, , )'
    break_list = []
    global repeat_no
    repeat_no -= 1


def push_rv(token):
    e = semantic_stack.pop()
    program_block.append(f'(ASSIGN, {e}, {rv_register}, )')


def return_func(token):
    if not declare_main:
        retrun_address_address = get_temp()
        program_block.append(f'(ADD, #4, {dp_register}, {retrun_address_address})')
        program_block.append(f'(ASSIGN, @{dp_register}, {dp_register}, )')
        retrun_address = get_temp()
        program_block.append(f'(ASSIGN, @{retrun_address_address}, {retrun_address}, )')
        program_block.append(f'(JP, @{retrun_address}, , )')


def push_id(token):
    lexeme = semantic_stack.pop()
    address, _scope = get_address(lexeme)
    temp = get_temp()
    if _scope == 'G':
        program_block.append(f'(ADD, {gp_register}, #{address}, {temp})')
    else:
        program_block.append(f'(ADD, {dp_register}, #{address + 8}, {temp})')

    semantic_stack.append(f'@{temp}')


def assign(token):
    op1 = semantic_stack.pop()
    op2 = semantic_stack[-1]
    program_block.append(f'(ASSIGN, {op1}, {op2}, )')


def push_arr(token):
    index = semantic_stack.pop()
    lexeme = semantic_stack.pop()
    address, _scope = get_address(lexeme)
    pointer_arr = get_temp()
    if _scope == 'G':
        program_block.append(f'(ADD, {gp_register}, #{address}, {pointer_arr})')
    else:
        program_block.append(f'(ADD, {dp_register}, #{address + 8}, {pointer_arr})')
    temp = get_temp()
    program_block.append(f'(MULT, #4, {index}, {temp})')
    final = get_temp()
    program_block.append(f'(ADD, @{pointer_arr}, {temp}, {final})')
    semantic_stack.append(f'@{final}')


def execute(token):
    op1 = semantic_stack.pop()
    operand = semantic_stack.pop()
    op2 = semantic_stack.pop()
    temp = get_temp()
    if operand == '+':
        program_block.append(f'(ADD, {op2}, {op1}, {temp})')
    elif operand == '*':
        program_block.append(f'(MULT, {op2}, {op1}, {temp})')
    elif operand == '-':
        program_block.append(f'(SUB, {op2}, {op1}, {temp})')
    elif operand == '==':
        program_block.append(f'(EQ, {op2}, {op1}, {temp})')
    else:
        program_block.append(f'(LT, {op2}, {op1}, {temp})')

    semantic_stack.append(str(temp))


def push_param(token):
    semantic_stack.append(['param'])


def store_arg(params):
    while params:
        e = params.pop()
        free_address = get_free_address()
        temp = get_temp()
        program_block.append(f'(ADD, {dp_register}, #{free_address + 8}, {temp})')
        program_block.append(f'(ASSIGN, {e}, @{temp}, )')


def extract_params(token):
    params = []
    while semantic_stack[-1] == ['param']:
        semantic_stack.pop()
        params.append(semantic_stack.pop())
    return params


def is_temp(name):
    if isinstance(name, str):
        return name.isnumeric() or (name[0] == '@' and name[1:].isnumeric())
    return False


def save_temps():
    addresses = []
    for var in semantic_stack:
        if is_temp(var):
            name = var if not var[0] == '@' else var[1:]
            free_address = get_free_address()
            temp = get_temp()
            program_block.append(f'(ADD, {dp_register}, #{free_address + 8}, {temp})')
            program_block.append(f'(ASSIGN, {name}, @{temp}, )')
            addresses.append(free_address)
    return addresses


def load_temps(addresses):
    i = 0
    for var in semantic_stack:
        if is_temp(var):
            name = var if not var[0] == '@' else var[1:]
            free_address = addresses[i]
            i += 1
            temp = get_temp()
            program_block.append(f'(ADD, {dp_register}, #{free_address + 8}, {temp})')
            program_block.append(f'(ASSIGN, @{temp}, {name}, )')


def call(token):
    params = extract_params(token)
    addresses = save_temps()
    lexeme = semantic_stack.pop()
    jump_address, _ = get_address(lexeme)
    free_address = get_free_address()
    new_dp = get_temp()
    program_block.append(f'(ADD, {dp_register}, #{free_address + 8}, {new_dp})')
    program_block.append(f'(ASSIGN, {dp_register}, @{new_dp}, )')

    free_address = get_free_address()
    return_address = get_temp()
    program_block.append(f'(ADD, {dp_register}, #{free_address + 8}, {return_address})')

    store_arg(params)

    program_block.append(f'(ASSIGN, {new_dp}, {dp_register}, )')
    here = len(program_block)
    program_block.append(f'(ASSIGN, #{here + 2}, @{return_address}, )')
    program_block.append(f'(JP, {jump_address}, , )')

    load_temps(addresses)
    temp = get_temp()
    program_block.append(f'(ASSIGN, {rv_register}, {temp}, )')
    semantic_stack.append(str(temp))


action_symbols = get_action_symbols()


def routines(st, nt, token, state, next_state):
    if st == 'return':
        next_state = state
    if (state, next_state) in action_symbols[nt]:
        for action in action_symbols[nt][(state, next_state)]:
            eval(action[1:] + '(token)')
    return
