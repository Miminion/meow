import re
s = input("Enter string: ")
pattern = r"^ab*$"
if re.match(pattern, s):
    print("Match")
else:
    print("No match")