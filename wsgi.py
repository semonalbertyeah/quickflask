import os,sys

if __name__ != '__main__':
    sys.path.insert(0, os.path.dirname(__file__))

from app import app as application

if __name__ == '__main__':
    application.run(host='0.0.0.0')
