KEYWORDS = ['if', 'else', 'void', 'int', 'repeat', 'break', 'until', 'return', 'endif']
SYMBOL_TABLE = {}
row = {'proc/func/var': '', 'No.arg/cell': 0, 'type': '', 'scope': ''}


def init_symbol_table():
    for keyword in KEYWORDS:
        SYMBOL_TABLE[keyword] = row


def add_to_symbol_table(lexeme):
    SYMBOL_TABLE[lexeme] = row
