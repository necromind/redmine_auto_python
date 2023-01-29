import os
import logging

from redminelib import Redmine
from app import settings
from app.helpers import class_factory

logger = logging.getLogger(__name__)


class RedmineApp:
    def __init__(self):
        self.redmine = Redmine(
            f'{settings.REDMINE_HOST}:{settings.REDMINE_PORT}',
            username=settings.REDMINE_USER,
            password=settings.REDMINE_PASSWORD
        )

    def run_tasks(self):
        """ Запускает все таски из папки tasks """
        dirname = os.path.dirname(os.path.abspath(__file__))+'/../tasks/'

        for f in os.listdir(dirname):
            if (f != "__init__.py" and os.path.isfile("%s/%s" % (dirname, f))
                    and f[-3:] == ".py"):
                task = class_factory(
                    f'tasks.{f[:-3]}.RedmineTask',
                    BaseRedmineTask,
                    redmine=self.redmine
                )
                if task.is_active:
                    task.run()

    def get_all_statuses(self):
        """ Печатает все статусы задач, чтобы узнать их id """
        statuses = self.redmine.issue_status.all()
        statuses_str = '\n'
        for status in statuses:
            statuses_str += f"'{status.name}': {str(status.id)},\n"
        logger.info(statuses_str)


class BaseRedmineTask:
    """ Базовый класс автоматической задачи """
    is_active = False

    projects_filter = ['*']
    projects_exclude = []

    def __init__(self, redmine):
        self.redmine = redmine

        if '*' in self.projects_filter:
            self.projects_filter = self.get_projects_ids()
        else:
            self.projects_filter = self.get_projects_ids(self.projects_filter)

        if self.projects_exclude:
            exclude_ids = self.get_projects_ids(self.projects_exclude)
            self.projects_filter = [
                f for f in self.projects_filter if f not in exclude_ids]

    def get_projects_ids(self, project_names=None):
        """ Возвращает список id проектов по их identifier """
        if project_names:
            ids = []
            for name in project_names:
                ids.append(self.redmine.project.get(name).id)
            return ids
        else:
            return list(
                self.redmine.project.all().values_list('id', flat=True))
