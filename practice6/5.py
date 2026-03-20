import os

if os.path.exists("practice6/data_backup.txt"):
    os.remove("practice6/data_backup.txt")
    print("Deleted")
else:
    print("File not found")