f = open('..\\tests\\PA1_input_output_samples\\T01\\input.txt', 'r')
EOF = ''

cursor = 0
c = f.read(1)
cursor += 1
while c:
    print(c, end='')
    c = f.read(1)
    cursor += 1
    if cursor == 27:
        f.seek(f.tell()-1, 0)
f.close()

print('Heeeeeeeeeeeeeeeeeeeeeeeeeeey')
print()

f = open('..\\tests\\PA1_input_output_samples\\T01\\input.txt', 'r')
print(f.read(6))

f.seek(f.tell()-1, 0)
print(f.read(1))
