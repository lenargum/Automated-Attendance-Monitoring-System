import random
from app import db


class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String())
    surname = db.Column(db.String())
    date = db.Column(db.String())
    
    def __init__(self, name, surname, date):
        self.name = name
        self.surname = surname
        self.date = date
    
    def __repr__(self):
        return '%s %s attend lecture at %s' % (self.name, self.surname, self.date)


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(), unique=True)
    expired = db.Column(db.Boolean)


class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bs_group = db.Column(db.String())
    name = db.Column(db.String())
    surname = db.Column(db.String())


def token_by_key(key):
    return Token.query.filter_by(key=key).first()


def add_attendance(bs_group, name, surname):
    print(bs_group, name, surname)
    att = Attendance(bs_group=bs_group, name=name, surname=surname)
    db.session.add(att)
    db.session.commit()


def reset_token():
    query = Token.query.filter_by(expired=False)
    
