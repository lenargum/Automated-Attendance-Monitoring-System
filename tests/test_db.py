from app import db
from app import models
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
def test_new_db():
    new_user = models.User(id=1001, name="Sample", surname="Man",
                           email="sample@sample.com", password_hash="123456", is_admin=False)
    db.session.add(new_user)
    db.session.commit()

    user = models.User.query.filter_by(id=1001).first_or_404()
    assert user.id == 1001
    assert user.name == "Sample"
    assert user.surname == "Man"
    assert user.email == "sample@sample.com"
    assert user.password_hash == "123456"
    assert user.is_admin == False
