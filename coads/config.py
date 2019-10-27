import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


class Config:
    DEBUG = False


class DevConfig(Config):
    DEBUG = True


class TestConfig(Config):
    DEBUG = True
    TESTING = True
    USER = 'user1'


class ProdConfig(Config):
    DEBUG = False


configs = dict(
    dev=DevConfig,
    test=TestConfig,
    prod=ProdConfig
)
