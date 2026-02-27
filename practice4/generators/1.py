def kvadrat(n):
    for i in range(n):
        yield i*i

a=int(input())
for x in kvadrat(a):
    print(x)