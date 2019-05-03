#!/usr/bin/env python3

from app import db
from app import models

session_types = [
    {"name": "Lecture"},
    {"name": "Tutorial"},
    {"name": "Lab"}
]

courses = [
    {"name": "[B17] Software Project"},
    {"name": "[B17] Probability and Statistics"},
    {"name": "[B17] Networks"}
]

roles = [
    {"name": "Student", "can_manage_sessions": 0},
    {"name": "TA", "can_manage_sessions": 1},
    {"name": "Professor", "can_manage_sessions": 1}
]

teachers = [
        {"name": "Vladimir", "surname": "Ivanov", "email": "v.ivanov@innopolis.ru", "password_hash": "pbkdf2:sha256:150000$7pCwLTDU$e954fc42bb4e69affa7cb4a1c8adf4ceb5afff22089c11aaea51c2b1bd70bea4", "is_admin": "false"}]

print("Adding Admin")
u = models.User(name="Admin", surname="Admin", email="none@mail", is_admin=True)
u.set_password(input("Enter Admin password: "))
db.session.add(u)
db.session.commit()
print("Admin Added")


print("Adding session types")
for session_type in session_types:
    print("Adding {}...".format(session_type["name"]))
    s = models.SessionType(**session_type)
    db.session.add(s)
    db.session.commit()
    print("Added")

print("Adding sample courses")
for course in courses:
    print("Adding {}...".format(course["name"]))
    c = models.Course(**course)
    db.session.add(c)
    db.session.commit()
    print("Added")

print("Adding roles")
for role in roles:
    r = models.Role(**role)
    db.session.add(r)
    db.session.commit()
    print("Added")
