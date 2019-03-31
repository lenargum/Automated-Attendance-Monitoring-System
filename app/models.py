from uuid import uuid4
from app import db
from flask_login import UserMixin
from app import login

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

session_student = db.Table("session_student",
                           db.Column("session_id", db.Integer, db.ForeignKey("session.id")),
                           db.Column("student_id", db.Integer, db.ForeignKey("user.id"))
                           )

student_courses = db.Table("student_courses",
                           db.Column("student_id", db.Integer, db.ForeignKey("user.id")),
                           db.Column("course_id", db.Integer, db.ForeignKey("course.id"))
                           )


# User model
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    surname = db.Column(db.String())
    email = db.Column(db.String(), unique=True)
    password_hash = db.Column(db.String(128))
    is_faculty = db.Column(db.Boolean)
    sessions = db.relationship("Session", secondary=session_student)
    courses = db.relationship('Course', secondary=student_courses)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Course model
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    faculty_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sessions = db.relationship('Session', backref='course', lazy=True)
    students = db.relationship('User', secondary=student_courses)


# Session model
class Session(db.Model):
    __tablename__ = "session"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    is_closed = db.Column(db.Boolean)
    tokens = db.relationship('Token', backref='session', lazy=True)
    faculty_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    students = db.relationship("User", secondary=session_student)


# Token model
class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(), unique=True)
    expired = db.Column(db.Boolean)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)


# Get token by key
def token_by_key(key):
    return Token.query.filter_by(key=key).first()

#
# # Add attendance entry
# def add_attendance(bs_group, name, surname):
#     att = Attendance(bs_group=bs_group, name=name, surname=surname)
#     db.session.add(att)
#     db.session.commit()


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
