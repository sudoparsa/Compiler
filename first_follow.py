def find_first():
    f = open('first', 'r')
    terminals = f.readline().split()
    a = {}
    terminals[-1] = 'epsilon'
    nterminals = []
    ff = open('c-minus_001.txt', 'r')
    for line in ff:
        nterminals.append(line.split()[0])
    print(terminals)

    for i in range(45):
        string = f.readline().split()
        nt = string[0]
        a[nterminals[i]] = []
        for j in range(len(string)):
            if string[j] == '+':
                a[nterminals[i]].append(terminals[j - 1])
    print(a)


def find_follow():
    f = open('follow', 'r')
    terminals = f.readline().split()
    a = {}
    terminals[-1] = ''
    nterminals = []
    ff = open('c-minus_001.txt', 'r')
    for line in ff:
        nterminals.append(line.split()[0])
    print(nterminals)

    for i in range(45):
        string = f.readline().split()
        nt = string[0]
        a[nterminals[i]] = []
        for j in range(len(string)):
            if string[j] == '+':
                a[nterminals[i]].append(terminals[j - 1])
    print(a)


find_first()
find_follow()
