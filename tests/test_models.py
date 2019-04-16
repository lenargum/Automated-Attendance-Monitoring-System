from app import models
from datetime import datetime

def test_new_session():
    """
    GIVEN a Session model
    WHEN a new Session is created
    THEN check the faculty_id, is_closed, type_id, and course_id fields are defined correctly
    """
    new_session = models.Session(date=datetime.now(),faculty_id=1,is_closed=False,
                                 type_id=2, course_id=3)
    assert new_session.faculty_id == 1
    assert new_session.is_closed == False
    assert new_session.type_id == 2
    assert new_session.course_id == 3



def test_new_course():
    """
    GIVEN a Course model
    WHEN a new Course is created
    THEN check the faculty_id, is, type_id, and name fields are defined correctly
    """
    new_course = models.Course(id=101, name= "SP", faculty_id=1001)
    assert new_course.faculty_id == 1001
    assert new_course.id == 101
    assert new_course.name == "SP"

def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the id, name, surname, email, password_hash and is_faculty fields are defined correctly
    """
    new_user = models.User(id=1001, name="Sample", surname="Man",
                                email="sample@sample.com", password_hash = "123456",  is_faculty = False)
    assert new_user.id == 1001
    assert new_user.name == "Sample"
    assert new_user.surname == "Man"
    assert new_user.email == "sample@sample.com"
    assert new_user.password_hash == "123456"
    assert new_user.is_faculty == False






