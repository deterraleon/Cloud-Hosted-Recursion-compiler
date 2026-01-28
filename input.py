def add(x, y):
    for i in range(y):
        x = x+1
    return x

def mult(x, y):
    nx = 0
    for i in range(y):
        nx = add(x, nx)
    return nx


inp = input().split()
x = inp[0]
y = inp[1]
z = inp[2]
x = int(x)
z = int(z)
if y == '+':
    w = add(x, z)
    print(w)
elif y == '*':
    w = mult(x, z)
    print(w)
elif y == '-':
    print(add(-z, x))
