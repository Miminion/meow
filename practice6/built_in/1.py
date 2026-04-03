from functools import reduce
n= [1, 2, 3, 4, 5]
s  = list(map(lambda x: x**2, n))
print(s)
e = list(filter(lambda x: x % 2 == 0, n))
print(e)

p = reduce(lambda x, y: x * y, n)
print(p)