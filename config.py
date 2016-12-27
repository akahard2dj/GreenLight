import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_ADMIN = 'master@bora.com'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASKY_POSTS_PER_PAGE = 30

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ['DEV_SQL_URI']


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ['TEST_SQL_URI']
    WTF_CSRF_ENABLED = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}