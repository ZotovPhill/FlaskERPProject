import os

from werkzeug.utils import import_string


class Config(object):
    APP_NAME = os.environ.get("APP_NAME", "FlaskERPProject")
    APP_VERSION = os.environ.get("APP_VERSION", "0.1")
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND")
    ROOT_PATH = os.environ.get("ROOT_PATH")
    CACHE_TYPE = os.environ["CACHE_TYPE"]
    CACHE_REDIS_HOST = os.environ["CACHE_REDIS_HOST"]
    CACHE_REDIS_PORT = os.environ["CACHE_REDIS_PORT"]
    CACHE_REDIS_DB = os.environ["CACHE_REDIS_DB"]
    CACHE_REDIS_URL = os.environ["CACHE_REDIS_URL"]
    CACHE_DEFAULT_TIMEOUT = os.environ["CACHE_DEFAULT_TIMEOUT"]


class ProductionConfig(Config):
    ENVIRONMENT = "prod"
    DEBUG = False
    SECRET_KEY = "9asdf8980as8df9809sf6a6ds4f3435fa64ˆGggd76HSD57hsˆSDnb"


class DevelopmentConfig(Config):
    ENVIRONMENT = "dev"
    DEBUG = True
    SECRET_KEY = "9asdf8980as8df9809sf6a6ds4f3435fa64ˆGggd76HSD57hsˆSDnb"
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class Settings(dict):
    def __init__(self, *args, **kwargs):
        super(Settings, self).__init__(*args, **kwargs)
        self.__dict__ = self

    @staticmethod
    def get_env_config():
        environment_configuration = os.environ["CONFIGURATION_SETUP"]
        return import_string(environment_configuration)

    @classmethod
    def create(cls):
        obj = cls.get_env_config()
        return cls(
            {key.lower(): getattr(obj, key) for key in dir(obj) if key.isupper()}
        )

    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, value):
        self.__dict__[attr.lower()] = value


settings = Settings.create()
