from datetime import date, timedelta

today = date.today()
keshe = today - timedelta(days=1)
erten  = today + timedelta(days=1)

print( keshe)
print( today)
print(erten)
