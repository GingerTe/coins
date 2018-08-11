import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SLOW_DB_QUERY_TIME = 0.5
    BOOTSTRAP_QUERYSTRING_REVVING = '4.1.3'
    BOOTSTRAP_USE_MINIFIED = True
    BOOTSTRAP_SERVE_LOCAL = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL',
                                             'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite'))


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL', 'sqlite://')
    WTF_CSRF_ENABLED = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,

    'default': DevelopmentConfig
}
