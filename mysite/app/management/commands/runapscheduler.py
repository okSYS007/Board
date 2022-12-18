import logging
 
from django.conf import settings
 
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from datetime import date, timedelta

from django.core.mail import EmailMultiAlternatives

from app.models import Announcement
from users.models import MyUser

from django.template.loader import render_to_string
 
logger = logging.getLogger(__name__)
 
 
# наша задача по выводу текста на экран
def my_job():
    
    startDay = date.today()+timedelta(days=-date.today().weekday())

    weekPosts = Announcement.objects.filter(Creation_date__gt = startDay)
    Users = MyUser.objects.values('username', 'email').exclude(username = 'admin')
    postInfo = []

    for post in weekPosts:
        postInfo.append(
            {
                'title': post.Announcement_title,
                'author': post.Announcement_author.username,
                'date': post.Creation_date,
                'postUrl': str(post.id)
            }
        )
    
    for Sub in Users:
        html_content = render_to_string( 
            'announce/weekly_mail.html',
            {
                'userName': Sub['username'],
                'postInfo': postInfo
            }
            )

        msg = EmailMultiAlternatives(
            subject=f'Еженедельная рассылка',
            body="", #  это то же, что и message
            from_email='ViacheslavDan803@gmail.com',
            to=[Sub['email']], # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html") # добавляем html

        msg.send() # отсылаем
 
 
# функция которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)
 
 
class Command(BaseCommand):
    help = "Runs apscheduler."
 
    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        
        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(
                #second="*/10"
                day_of_week="sun", hour="00", minute="00"),  
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")
 
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )
 
        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")