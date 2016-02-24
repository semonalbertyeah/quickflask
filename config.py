class Config(object):
    # secret key
    # a proper way to generate secret key:
    #   import os
    #   os.urandom(22) # generate random string with the length of 22
    SECRET_KEY = 'A_random_unique_key'

    # session 
    SESSION_COOKIE_NAME = 'qckflsk_sessions'
    SESSION_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = 60 * 60 * 24

    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = \
        'mysql+pymysql://cloudfs_web:123456@localhost/cloudfs_web_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Session
    SESSION_TYPE = 'sqlalchemy'
    SESSION_SQLALCHEMY = None   # remember to manually provide a floask.ext.sqlalchemy.SQLAlchemy instance with Flask-SQLAlchemy config above
    SESSION_SQLALCHEMY_TABLE = 'quickflask_sessions'
    SESSION_USE_SIGNER = True

    # sqlite session
    SQLITE_SESSION_DIR = 'usr_sessions'
