s = input("Enter snake_case string: ")
parts = s.split("_")
camel = parts[0] + "".join(word.capitalize() for word in parts[1:])
print("CamelCase:", camel)