s = input("Enter text: ")
result = re.sub(r"([A-Z])", r" \1", s).strip()
print("Result:", result)