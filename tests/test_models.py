from app import models
from datetime import datetime

def test_new_session():
    """
    GIVEN a Session model
    WHEN a new Session is created
    THEN check the faculty_id, is_closed, type_id, and course_id fields are defined correctly
    """
    new_session = models.Session(date=datetime.now(),
                                 faculty_id=1,
                                 is_closed=False,
                                 type_id=2,
                                 course_id=3)
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
    new_session = models.Course(id = 101, name= "SP", faculty_id=1001)
    assert new_session.faculty_id == 1001
    assert new_session.id == 101
    assert new_session.name == "SP"

