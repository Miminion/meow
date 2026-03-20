import shutil

shutil.move("data.txt", "project/data/data.txt")
shutil.copy("project/data/data.txt", "project/backup/data.txt")