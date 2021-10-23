f = open('..\\tests\\T01\\input.txt', 'r')
EOF = ''

cursor = 0
c = f.read(1)
cursor += 1
while c != EOF:
    print(c, end='')
    c = f.read(1)
    cursor += 1
    if cursor == 27:
        f.seek(f.tell()-1, 0)
