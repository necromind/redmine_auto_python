import logging
import datetime

from app.redmine import BaseRedmineTask
from app.defaults import STATUSES


logger = logging.getLogger(__name__)


class RedmineTask(BaseRedmineTask):
    """ Автоматическая задача на закрытие старых(<days_ago) задач
    со статусом open """

    is_active = True
    projects_filter = ['*']
    projects_exclude = []
    days_ago = 30
    old_status = STATUSES['Open']
    new_status = STATUSES['Закрыта']
    add_note = f'Issue auto closed after {days_ago} days.'

    def run(self):
        logger.info('Run')
        month_ago = datetime.date.today() - datetime.timedelta(
            days=self.days_ago)

        for project in self.projects_filter:
            issues = self.redmine.issue.filter(
                project_id=project,
                created_on=f'<={month_ago.strftime("%Y-%m-%d")}',
                status_id=self.old_status
            ).update(
                status_id=self.new_status,
                notes=self.add_note
            )
            if len(issues) > 0:
                logger.info(f'{str(len(issues))} issues closed.')
