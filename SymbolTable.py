SYMBOL_TABLE = []
global_address = 0
local_address = 0


def add_to_symbol_table(lexeme, type, scope, func, func_address):
    global global_address, local_address
    if scope == 'G':
        address = global_address
        global_address += 4
    else:
        address = local_address
        local_address += 4
    func_var = 'var'
    if func:
        func_var = 'func'
        address = func_address

    SYMBOL_TABLE.append(
        {'lexeme': lexeme, 'func/var': func_var, 'No.arg/cell': 0, 'type': type, 'scope': scope, 'address': address})


def get_table_address(lexeme):
    global SYMBOL_TABLE
    for symbol in SYMBOL_TABLE[::-1]:
        if symbol['lexeme'] == lexeme:
            return symbol['address'], symbol['scope']
    return False


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
