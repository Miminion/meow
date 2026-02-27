from datetime import datetime

d1 = datetime(2026, 1, 1, 0, 0, 0)
d2 = datetime(2026, 2, 27, 10, 45, 30)

airma = d2 - d1
sec = airma.total_seconds()

print( d1)
print(d2)
print(sec)