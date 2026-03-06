import re
text = input("Enter text: ")
pattern = r"\b[a-z]+_[a-z]+\b"
matches = re.findall(pattern, text)
print("Matches:", matches)