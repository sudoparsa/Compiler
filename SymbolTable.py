SYMBOL_TABLE = []
global_address = 0
local_address = 0


def add_to_symbol_table(lexeme, type, scope, func, func_address, arr):
    global global_address, local_address
    if scope == 'G':
        address = global_address
        global_address += 4
    else:
        address = local_address
        local_address += 4
    func_var_arr = 'var'
    if func:
        func_var_arr = 'func'
        address = func_address
    elif arr:
        func_var_arr = 'arr'

    SYMBOL_TABLE.append(
        {'lexeme': lexeme, 'func/var/arr': func_var_arr, 'No.arg/cell': 0, 'type': type, 'scope': scope,
         'address': address})


def get_table_address(lexeme):
    global SYMBOL_TABLE
    for symbol in SYMBOL_TABLE[::-1]:
        if symbol['lexeme'] == lexeme:
            return symbol['address'], symbol['scope']
    return False, 'error'


def get_table_free_address():
    global local_address
    local_address += 4
    return local_address - 4


def table_reset_scope():
    global SYMBOL_TABLE, local_address
    temp_table = []
    for symbol in SYMBOL_TABLE:
        if symbol['scope'] == 'G':
            temp_table.append(symbol)
    SYMBOL_TABLE = temp_table
    local_address = 0


def set_table_arr(lexeme):
    global SYMBOL_TABLE
    for symbol in SYMBOL_TABLE[::-1]:
        if symbol['lexeme'] == lexeme:
            symbol['func/var/arr'] = 'arr'
            return


def set_func_args(lexeme, args_lexeme):
    global SYMBOL_TABLE
    args_type = []
    for arg in args_lexeme:
        args_type.append(get_type(arg))
    for symbol in SYMBOL_TABLE[::-1]:
        if symbol['lexeme'] == lexeme:
            symbol['No.arg/cell'] = args_type
            return


def get_func_args(lexeme):
    global SYMBOL_TABLE
    for symbol in SYMBOL_TABLE[::-1]:
        if symbol['lexeme'] == lexeme:
            return symbol['No.arg/cell']


def get_type(lexeme):
    global SYMBOL_TABLE
    for symbol in SYMBOL_TABLE[::-1]:
        if symbol['lexeme'] == lexeme:
            return symbol['func/var/arr']
