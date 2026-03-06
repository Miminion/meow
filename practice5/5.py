import re
s = input("Enter string: ")
pattern = r"^a.*b$"
if re.match(pattern, s):
    print("Match")
else:
    print("No match")