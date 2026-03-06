s = input("Enter camelCase or PascalCase string: ")
result = re.split(r"(?=[A-Z])", s)
print("Split:", result)