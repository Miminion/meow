import os
l = os.listdir("project")

for i in l:
    if os.path.isdir("project/" + i):
        print( i)
    else:
        print(i)