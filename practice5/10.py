s = input("Enter camelCase string: ")
snake = re.sub(r"([A-Z])", r"_\1", s).lower().lstrip("_")
print("Snake_case:", snake)