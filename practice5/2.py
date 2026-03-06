import re 
s = input("Enter string: ")
pattern = r"^ab{2,3}$"
if re.match(pattern, s):
    print("Match")
else:
    print("No match")