#!/usr/bin/env python3

import os
from app import db
from app import models
from app import app

if app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite"):
    print("Using SQLite; simply removing file...")
    try:
        os.remove("app.db")
        print("Done")
    except FileNotFoundError:
        print("File not found, skipping")
else:
    print("Dropping all tables...")
    db.drop_all()
    print("Done ")

print("Creating tables...")
db.create_all()
print("Creating tables done")
