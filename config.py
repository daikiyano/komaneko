import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir,'.env'))

class Config(object):
    DEBUG=False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")


class DevelopmentConfig(Config):
    DEVELOPMENT = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
    AWS_BUCKET = os.environ.get("AWS_BUCKET")


class StagingConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    AWS_BUCKET = os.environ.get("AWS_BUCKET")

class ProductionConfig(Config):
    DEBUG = False
    AWS_BUCKET = os.environ.get("AWS_BUCKET_PRODUCTION")
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
