from preprocess2 import get_action_table
from Scanner import get_next_token
from anytree import Node, RenderTree


def get_look_ahead(file, lineno):
    token, state, character, lineno, token_lineno = get_next_token(file, lineno)
    if state >= 0 and token is not None:  # No Lexical Error
        type, lexeme = token
        if type == 'ID' or type == 'NUM':
            return type, lineno, token_lineno
        return lexeme, lineno, token_lineno
    if not character:
        return '$', lineno, token_lineno
    get_look_ahead(file, lineno)


def parse(file_path='input.txt'):
    file = open(file_path, 'r')
    stack = [('Program', 0)]
    action_table = get_action_table()
    lineno = 1
    root = Node('Program')
    look_ahead, lineno, token_lineno = get_look_ahead(file, lineno)
    while True:
        nt, state = stack.pop()
        if (nt, state, look_ahead) not in action_table.keys():  # Goal State
            action = ['return']
        else:
            action = action_table[(nt, state, look_ahead)].split()

        if action[0] == 'return':
            nt, state, next_state = stack.pop()
            stack.append((nt, next_state))

        if action[0] == 'goto':
            next_state = action[1]
            stack.append((nt, next_state))
            node = Node(look_ahead, parent=nt)
            look_ahead, lineno, token_lineno = get_look_ahead(file, lineno)

        if action[0] == 'call':
            tk = action[1]
            next_state = action[2]

        if action[0] == 'missing':
            tk = action[1]
            next_state = action[2]

        if action[0] == 'illegal':
            t = action[1]
            next_state = action[2]



    file.close()
