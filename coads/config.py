from os.path import join, dirname
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


@dataclass
class Config:
    DEBUG = False


@dataclass
class DevConfig(Config):
    DEBUG = True


@dataclass
class TestConfig(Config):
    DEBUG = True
    TESTING = True
    USER = 'user1'


@dataclass
class ProdConfig(Config):
    DEBUG = False


configs = dict(
    dev=DevConfig,
    test=TestConfig,
    prod=ProdConfig
)
