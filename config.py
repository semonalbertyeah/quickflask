from datetime import timedelta

class Config(object):
    # secret key
    # a proper way to generate secret key:
    #   import os
    #   os.urandom(22) # generate random string with the length of 22
    SECRET_KEY = 'A_random_unique_key'

    # session 
    SESSION_COOKIE_NAME = 'qckflsk_sessions'
    SESSION_COOKIE_HTTPONLY = True
    #PERMANENT_SESSION_LIFETIME = 60 * 60 * 24
    PERMANENT_SESSION_LIFETIME = timedelta(1)   # some flask session extensions do not support int

    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = \
        'mysql+pymysql://qckflsk:123456@localhost/quickflask'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Session
    SESSION_TYPE = 'sqlalchemy'
    SESSION_SQLALCHEMY = None   # remember to manually provide a floask.ext.sqlalchemy.SQLAlchemy instance with Flask-SQLAlchemy config above
    SESSION_SQLALCHEMY_TABLE = 'quickflask_sessions'
    SESSION_USE_SIGNER = True

    # Flask-KVSession
    # use default
    # custom Flask-KVSession config
    KVSESSION_DATABASE_URI = \
        'mysql+pymysql://qckflsk:123456@localhost/quickflask'
    KVSESSION_DATABASE_TABLE = 'quickflask_kvsessions'

