import os


class BaseConfig:
    GITHUB_API = ''
    TOKEN = ''


class TestConfig(BaseConfig):
    GITHUB_API = 'https://api.github.com'
    TOKEN = os.environ['GITHUB_TOKEN']


class DevConfig(BaseConfig):
    GITHUB_API = 'https://api.dev.github.com'
    TOKEN = os.environ['GITHUB_TOKEN']


class ProdConfig(BaseConfig):
    GITHUB_API = 'https://api.github.com'
    TOKEN = os.environ['GITHUB_TOKEN']


class LocalConfig(DevConfig):
    GITHUB_API = 'https://api.github.com'
    TOKEN = os.environ['GITHUB_TOKEN']


CONFIG = {
    'TEST': TestConfig,
    'LOCAL': LocalConfig,
    'DEFAULT': TestConfig,
    'DEVELOPMENT': DevConfig,
    'PRODUCTION': ProdConfig,
}


def get_configuration():
    environment = os.getenv('ENV', 'DEFAULT')
    return CONFIG[environment]
