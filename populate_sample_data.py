#!/usr/bin/env python3

from app import db
from app import models

session_types = [
    {"name": "Lecture"},
    {"name": "Tutorial"},
    {"name": "Lab"}
]

courses = [
    {"name": "[B17] Software Project", "faculty_id": 1},
    {"name": "[B17] Probability and Statistics", "faculty_id": 1},
    {"name": "[B17] Networks", "faculty_id": 1}
]

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
