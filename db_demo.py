from app import db
from app import models

print("Users filename: ")
filename = input()
for person in open(filename, "r").readlines():
    data = person.split(" ")
    u = models.User(name=data[0], surname=data[1], email=data[2], is_faculty=False)
    u.set_password("test")
    db.session.add(u)
try:
    db.session.commit()
except Exception:
    print("[Error] DB already has this users.\nReverting changes...")
