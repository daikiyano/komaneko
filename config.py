import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir,'.env'))



###############################################
#############Configuration for all Stage#######
###############################################

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
    GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
    ADMIN_NAME = os.environ.get("ADMIN_NAME")
    RECAPTCHA_PUBLIC_KEY = os.environ.get("RECAPTCHA_PUBLIC_KEY")
    RECAPTCHA_PRIVATE_KEY = os.environ.get("RECAPTCHA_PRIVATE_KEY")
    RECAPTCHA_USE_SSL = False


#############Configuration for Development##################
class DevelopmentConfig(Config):
    DEVELOPMENT = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
    AWS_BUCKET = os.environ.get("AWS_BUCKET")


#############Configuration for Staging##################

class StagingConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    AWS_BUCKET = os.environ.get("AWS_BUCKET")


#############Configuration for Production##################

class ProductionConfig(Config):
    DEBUG = False
    AWS_BUCKET = os.environ.get("AWS_BUCKET_PRODUCTION")
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
