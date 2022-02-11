import os

class Config(object):
    YNAB_URL = os.environ['YNAB_URL']
    DATABASE_URL = os.environ['DATABASE_URL']
    BEARER = os.environ['BEARER']
    # ERROR_LOGGING_FILE = 'error_log.txt'