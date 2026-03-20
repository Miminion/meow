import os
for i in os.listdir("."):
    if i.endswith(".txt"):
        print(i)