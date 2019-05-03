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
        {"name": "Vladimir", "surname": "Ivanov", "email": "v.ivanov@innopolis.ru", "password_hash": "pbkdf2:sha256:150000$7pCwLTDU$e954fc42bb4e69affa7cb4a1c8adf4ceb5afff22089c11aaea51c2b1bd70bea4", "is_admin": 0},
        {"name": "Ivan", "surname": "Vladimirov", "email": "i.kalinin@innopolis.ru", "password_hash": "pbkdf2:sha256:150000$7pCwLTDU$e954fc42bb4e69affa7cb4a1c8adf4ceb5afff22089c11aaea51c2b1bd70bea4", "is_admin": 0}]


print("Adding Admin")
u = models.User(name="Admin", surname="Admin", email="admin@innopolis.ru", is_admin=True)
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
    print("Adding {}...".format(role["name"]))
    r = models.Role(**role)
    db.session.add(r)
    db.session.commit()
    print("Added")

print("Adding TAs")
for ta in teachers:
    print("Adding {} {}...".format(ta["name"], ta["surname"]))
    t = models.User(**ta)
    db.session.add(t)
    db.session.commit()
    print("Added")

print("Assigning TAs to the courses")
ta_id = 1
for ta in teachers:
    ta_id += 1
    course_id = 1
    for course in courses:
        print("Assigning {} {} to the {}...".format(ta["name"], ta["surname"], course["name"]))
        enrollment = {}
        enrollment["user"] = ta_id
        enrollment["course"] = course_id
        enrollment["role"] = 2
        print(enrollment)
        e = models.Enrollment(**enrollment)
        db.session.add(e)
        db.session.commit()
        print("Added")
        course_id += 1

