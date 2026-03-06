text = input("Enter text: ")
pattern = r"\b[A-Z][a-z]+\b"
matches = re.findall(pattern, text)
print("Matches:", matches)
#5