def dai(n):
    for i in range(n,-1,-1):
        yield i
a=int(input())
for x in dai(a):
    print(x)