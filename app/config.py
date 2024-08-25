import os

class Configuration:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ConfigTest:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'  # Use SQLite for testing
    SQLALCHEMY_TRACK_MODIFICATIONS = False
