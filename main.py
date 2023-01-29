import logging

from app import settings
from app.redmine import RedmineApp


logging.basicConfig(format=settings.LOGGER_FORMAT, level=logging.INFO)


if __name__ == '__main__':
    logging.getLogger('redmine_auto').setLevel(logging.DEBUG)

    redmine_app = RedmineApp()
    redmine_app.run_tasks()
    # redmine_app.get_all_statuses()
