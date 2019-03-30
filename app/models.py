from uuid import uuid4
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
    
    def serialize(self):
        return {
                'id': self.id,
                'name': self.name,
                'surname': self.surname,
                'date': self.date
                }

# User model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    surname = db.Column(db.String())
    email = db.Column(db.String(), unique=True)
    isFaculty = db.Column(db.Boolean)
    courses = db.relationship('Course', backref='user', lazy=True)
    sessions = db.relationship('Session', backref='user', lazy=True)
    sessionStudents = db.relationship('SessionStudent', backref='user', lazy=True)

# Course model
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    sessions = db.relationship('Session', backref='course', lazy=True)
    facultyId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Session model
class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    courseName = db.Column(db.String())
    sessionStudents = db.relationship('SessionStudent', backref='session', lazy=True)
    tokens = db.relationship('Token', backref='session', lazy=True)
    facultyId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    courseId = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

# SessionStudent model
class SessionStudent(db.Model):
    studentId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sessionId = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)


# Token model
class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(), unique=True)
    expired = db.Column(db.Boolean)
    sessionId = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)


# Attendance model
class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bs_group = db.Column(db.String())
    name = db.Column(db.String())
    surname = db.Column(db.String())


# Get token by key
def token_by_key(key):
    return Token.query.filter_by(key=key).first()


# Add attendance entry
def add_attendance(bs_group, name, surname):
    att = Attendance(bs_group=bs_group, name=name, surname=surname)
    db.session.add(att)
    db.session.commit()


# Expire all tokens and add new one
def reset_token():
    fresh_tokens = Token.query.filter_by(expired=False).paginate().items
    for token in fresh_tokens:
        token.expired = True
    db.session.commit()
    new_token = Token(key=str(uuid4()), expired=False)
    db.session.add(new_token)
    db.session.commit()


# Get any non-expired token
def get_token():
    return Token.query.filter_by(expired=False).first()
