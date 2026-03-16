import urllib.parse
import os

class DevelopmentConfig:
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = urllib.parse.quote_plus(os.getenv("MYSQL_PASSWORD", ""))
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@localhost/{MYSQL_DATABASE}"
    )
    DEBUG = True
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 300

class TestingConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 300

class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    CACHE_TYPE = "SimpleCache"
