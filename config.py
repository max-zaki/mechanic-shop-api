import urllib.parse
import os
from dotenv import load_dotenv

load_dotenv()

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
    pass

class ProductionConfig:
    pass
