SYMBOL_TABLE = {}
global_address = 0
local_address = 0


def add_to_symbol_table(lexeme, type, scope, func=False):
    func_var = 'var'
    if func:
        func_var = 'func'
    global global_address, local_address
    if scope == 'G':
        global_address += 4
        address = global_address
    else:
        local_address += 4
        address = local_address

    SYMBOL_TABLE[lexeme] = {'func/var': func_var, 'No.arg/cell': 0, 'type': type, 'scope': scope, 'address': address}


def get_table_address(lexeme):
    global SYMBOL_TABLE
    return SYMBOL_TABLE[lexeme]['address'], SYMBOL_TABLE[lexeme]['scope']


def get_table_free_address():
    global local_address
    local_address += 4
    return local_address - 4


def table_reset_scope():
    global SYMBOL_TABLE, local_address
    temp_table = {}
    for lexeme, row in SYMBOL_TABLE.items():
        if row['scope'] == 'G':
            temp_table[lexeme] = row
    SYMBOL_TABLE = temp_table
    local_address = 0
