import os


class BaseConfig:
    TOKEN = ''
    GITHUB_API = ''


class TestConfig(BaseConfig):
    TOKEN = os.environ['GITHUB_TOKEN']
    GITHUB_API = 'https://api.github.com'


class DevConfig(BaseConfig):
    TOKEN = os.environ['GITHUB_TOKEN']
    GITHUB_API = 'https://api.dev.github.com'


class ProdConfig(BaseConfig):
    TOKEN = os.environ['GITHUB_TOKEN']
    GITHUB_API = 'https://api.github.com'


class LocalConfig(DevConfig):
    TOKEN = os.environ['GITHUB_TOKEN']
    GITHUB_API = 'https://api.github.com'


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
