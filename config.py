"""Looks in the environment to check whether or no it's being run in production
or development and set the correct configuration base on that.

"""

import os
import yaml


def relative_filepath(filepath):
    """Joins a path string to the directory of this file"""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)


def get_template_folder(app_subdomain):
    return relative_filepath(
        '../{}/{}/'.format(app_subdomain, PATH_SUB_DIR))


config_path = relative_filepath('config')

environment = os.environ.get('APP_ENV', 'development')

virtual_host = os.environ.get('VIRTUAL_HOST')
app_subdomain = virtual_host.split('.')[0]

load_config_file = lambda f: yaml.load(open(os.path.join(config_path, f), 'r'))

configuration = {}
configuration.update(load_config_file("environment/{}.yml".format(environment)))

db_config = configuration['database']

app_secret = os.environ.get('APP_SECRET') or configuration['app_secret']

cache_dir = configuration.get('cache_dir') or relative_filepath('./cache')

# Flask Settings
PATH_SUB_DIR = environment == 'production' and 'dist' or 'app'

PROJECT_ROOT = os.path.abspath(os.path.split(__file__)[0])
TEMPLATE_FOLDER = get_template_folder(app_subdomain)
STATIC_URL_PATH = ''
STATIC_FOLDER = TEMPLATE_FOLDER
CACHE_TIMEOUT = 60 * 60 * 24


def configure_logger():
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'console': {
                'format': '[%(asctime)s][%(levelname)s] %(name)s %(filename)s:%(funcName)s:%(lineno)d:%(threadName)s | %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'console'
            },
            'sentry': {
                'level': 'ERROR',
                'class': 'raven.handlers.logging.SentryHandler',
                'dsn': os.environ.get('SENTRY_DSN') or configuration['sentry_dsn'],
            },
        },
        'loggers': {
            '': {
                'handlers': ['console', 'sentry'],
                'level': 'INFO',
                'propagate': False,
            },
        }
    }
    from logging.config import dictConfig
    dictConfig(LOGGING)


configure_logger()
