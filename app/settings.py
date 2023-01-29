import os
from dotenv import load_dotenv

load_dotenv()

LOGGER_FORMAT = os.getenv(
    'LOGGER_FORMAT',
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

REDMINE_HOST = os.getenv('REDMINE_HOST')
REDMINE_PORT = os.getenv('REDMINE_PORT')
REDMINE_USER = os.getenv('REDMINE_USER')
REDMINE_PASSWORD = os.getenv('REDMINE_PASSWORD')
