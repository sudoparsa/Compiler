rv_register = 450
dp_register = 454
gp_register = 458
ap_register = 462

temp_pointer = 3000
initial = True



program_block = [
    f'(ASSIGN, #0, {rv_register}, )',
    f'(ASSIGN, #500, {dp_register}, )',
    f'(ASSIGN, #15000, {gp_register}, )',
    f'(ASSIGN, #20000, {ap_register}, )'
]

semantic_stack = []

break_list = []


symbol_table = []

def add_symbol_id(lexme, type, scope, func=False):
    pass

def get_address(lexeme):
    pass

def get_free_address():
    pass

def reset_scope():
    pass

scope = 'G'

def get_temp():
    global temp_pointer
    temp_pointer += 4
    return temp_pointer - 4
def push_token(token):
    semantic_stack.append(token)

def declare_id(token, arg=False):
    lexeme = semantic_stack.pop()
    type = semantic_stack.pop()
    add_symbol_id(lexeme, type, scope)

    if not arg:
        temp = get_temp()
        address, _scope = get_address(lexeme)
        if scope == 'G':
            program_block.append(f'(ADD, {gp_register}, #{address}, {temp})')
        else:
            program_block.append(f'(ADD, {dp_register}, #{address + 8}, {temp})')
        program_block.append(f'(ASSIGN, #0, {temp})')

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
    add_symbol_id(lexeme, type, scope)
    temp = get_temp()
    address, _scope = get_address(lexeme)

    if scope == 'G':
        program_block.append(f'(ADD, {gp_register}, #{address}, {temp})')
    else:
        program_block.append(f'(ADD, {dp_register}, #{address + 8}, {temp})')

    program_block.append(f'(ASSIGN, {ap_register}, @{temp}, )')
    assign_array_memory(length)

def new_scope(token):
    scope = 'L'

def end_scope(token):
    scope = 'G'
    reset_scope()

def fill_jump():
    i = semantic_stack.pop()
    here = len(program_block)
    program_block[i] = f'(JP, {here}, , )'

def save(token):
    semantic_stack.append(len(program_block))
    program_block.append("")

def declare_func(token):
    lexeme = semantic_stack.pop()
    type = semantic_stack.pop()
    add_symbol_id(lexeme, type, 'G', func=True)
    if not lexeme == 'main':
        save(token)

def pop(token):
    semantic_stack.pop()
    

def break_until(token):
    break_list.append(len(program_block))
    program_block.append("")

def jpf_save(token):
    i = semantic_stack.pop()
    e = semantic_stack.pop()
    here = len(program_block)
    semantic_stack.append(here)

    program_block[i] = f'(JPF, {e}, {here + 1}, )' 

def label(token):
    here = len(program_block)
    semantic_stack.append(here)

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

def push_rv(token):
    e = semantic_stack.pop()
    program_block.append(f'(ASSIGN, {e}, {rv_register}, )')

def return_func(token):
    retrun_address_address = get_temp()
    program_block.append(f'(ADD, #4, {dp_register}, {retrun_address_address})')
    program_block.append(f'(ASSIGN, @{dp_register}, {dp_register}')
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
    op1 = semantic_stack.append()
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
    program_block.append(f'(ADD, {pointer_arr}, {temp}, {final})')
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

    semantic_stack.append(temp)

def store_reserve(token):
    lexeme = semantic_stack.pop()
    address, _scope = get_address(lexeme)
    semantic_stack.append(address)
    free_address = get_free_address()
    temp = get_temp()
    program_block.append(f'(ADD, {dp_register}, #{free_address + 8}, {temp})')
    program_block.append(f'(ASSIGN, {dp_register}, @{temp}, )')
    semantic_stack.append(temp)

    free_address = get_free_address()
    temp = get_temp()
    program_block.append(f'(ADD, {dp_register}, #{free_address + 8}, {temp})')
    semantic_stack.append(f'@{temp}')

def store_arg(token):
    e = semantic_stack.pop()
    free_address = get_free_address()
    temp = get_temp()
    program_block.append(f'(ADD, {dp_register}, #{free_address + 8}, {temp})')
    program_block.append(f'(ASSIGN, {e}, @{temp}, )')

def call(token):
    return_address = semantic_stack.pop()
    dp_address = semantic_stack.pop()
    jump_address = semantic_stack.pop()
    program_block.append(f'(ASSIGN, {dp_address}, {dp_register}, )')
    here = len(program_block)
    program_block.append(f'(ASSIGN, #{here + 2}, {return_address}, )')
    program_block.append(f'(JP, {jump_address}, , )')




    








    




    


    
