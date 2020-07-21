import os

APP_ROOT = os.path.dirname(os.path.abspath(
    __file__))
APP_STATIC = os.path.join(APP_ROOT, 'static/image')
JWT_SECRET_KEY = str(os.environ.get("JWT_SECRET_KEY"))
HOST = str(os.environ.get("DB_HOST"))
DATABASE = str(os.environ.get("DB_DATABASE"))
USERNAME = str(os.environ.get("DB_USERNAME"))
PASSWORD = str(os.environ.get("DB_PASSWORD"))
CHARSET = str(os.environ.get("DB_CHARSET"))
DB_URI = "mysql+pymysql://%s:%s@%s:3306/%s?charset=%s" % (
    USERNAME, PASSWORD, HOST, DATABASE, CHARSET)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_RECORD_QUERIES = True
