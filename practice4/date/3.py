from datetime import datetime

kaz = datetime.now()
print(kaz)

nomisec= kaz.replace(microsecond=0)
print(nomisec)