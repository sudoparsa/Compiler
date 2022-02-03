from code_gen import *
from preprocess import get_action_table
from Scanner import get_next_token
from anytree import Node, RenderTree


def get_look_ahead(token):
    type, lexeme = token
    if type == 'ID' or type == 'NUM':
        return type
    return lexeme


def get_token(file, lineno):
    token, state, character, lineno, token_lineno = get_next_token(file, lineno)
    if state >= 0 and token is not None:  # No Lexical Error
        return token, get_look_ahead(token), lineno, token_lineno
    if not character:  # EOF
        return '$', '$', lineno, token_lineno
    return get_token(file, lineno)


def parse(file_path='input.txt'):
    file = open(file_path, 'rb')
    root = Node('Program')
    stack = [(root, 0, 1)]
    action_table = get_action_table('grammar.txt')
    lineno = 1
    token, look_ahead, lineno, token_lineno = get_token(file, lineno)
    errors = []
    while True:
        node, state, next_state = stack.pop()
        nt = node.name
        if (nt, state, look_ahead) not in action_table.keys():  # Goal State
            action = ['return']
        else:
            action = action_table[(nt, state, look_ahead)].split()

        if action[0] == 'return':
            temp = token
            if token == '$':
                temp = '$$'
            routines(action[0], nt, temp[1], state, next_state)
            if token == '$' and nt == 'Program':
                break
            node, state, next_state = stack.pop()
            stack.append((node, next_state, 0))

        if action[0] == 'goto':
            tk = action[1]
            if tk != 'epsilon':
                tk = token
            next_state = int(action[2])
            temp = tk
            if token == '$':
                temp = '$$'
            routines(action[0], nt, temp[1], state, next_state)
            stack.append((node, next_state, 0))
            Node(tk, parent=node)
            if tk != 'epsilon':
                token, look_ahead, lineno, token_lineno = get_token(file, lineno)

        if action[0] == 'call':
            tk = action[1]
            next_state = int(action[2])
            temp = token
            if token == '$':
                temp = '$$'
            routines(action[0], nt, temp[1], state, next_state)
            stack.append((node, state, next_state))
            stack.append((Node(tk, parent=node), 0, 0))

        if action[0] == 'missing':
            tk = action[1]
            next_state = int(action[2])
            errors.append(f'#{token_lineno} : syntax error, missing {tk}')
            stack.append((node, next_state, 0))

        if action[0] == 'illegal':
            tk = action[1]
            next_state = int(action[2])
            if look_ahead == '$':
                errors.append(f'#{token_lineno} : syntax error, Unexpected EOF')
                break
            else:
                errors.append(f'#{token_lineno} : syntax error, illegal {tk}')
            stack.append((node, state, next_state))
            token, look_ahead, lineno, token_lineno = get_token(file, lineno)

    out_file = open('output.txt', 'w')
    for i in range(len(program_block)):
        out_file.write(f'{i}\t{program_block[i]}\n')
    out_file.close()
    file.close()

    save2txt(root, errors)
    return


def save2txt(root, errors):
    out = open('parse_tree.txt', 'w', encoding='utf-8')
    res = ''
    for pre, fill, node in RenderTree(root):
        res = res + "%s%s" % (pre, node.name) + '\n'
    res = res.replace("'", '')
    out.write(res[:-1])
    out.close()

    out = open('syntax_errors.txt', 'w', encoding='utf-8')
    res = ''
    for e in errors:
        res = res + e + '\n'
    if res == '':
        res = 'There is no syntax error.'
    out.write(res)
    out.close()


if __name__ == '__main__':
    parse()
