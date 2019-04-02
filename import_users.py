#!/usr/bin/env python3

import sys
from app import db
from app import models

if len(sys.argv) != 2:
    print("Usage: {} INPUT".format(sys.argv[0]))
    sys.exit(1)

try:
    with open(sys.argv[1], "r") as f:
        lines = f.readlines()
except FileNotFoundError as e:
    print("{}: file not found".format(sys.argv[1]))
    sys.exit(1)

for line in lines:
    data = line.strip().split(" ")
    name = data[0]
    surname = data[1]
    email = data[2]
    if models.User.query.filter_by(email=email).first():
        print("Cannot add user {} {} ({}): email already in database".format(name, surname, data))
        continue
    u = models.User(name=name, surname=surname, email=email, is_faculty=False)
    u.set_password("test")
    db.session.add(u)
    db.session.commit()
    print("Added user {} {} ({})".format(name, surname, data))
