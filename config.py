import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SERVER_NAME = os.environ.get('SERVER_NAME') or "127.0.0.1:5000"
    SERVER_URL = os.environ.get('SERVER_URL') or "127.0.0.1:5000"
