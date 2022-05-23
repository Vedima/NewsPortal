import logging
import datetime
from django.core.mail import send_mail
from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from ...models import Post, User
from django.utils.timezone import make_aware
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


# наша задача по рассылке писем
def my_job():
    print(datetime.datetime.today().weekday())
    #if datetime.datetime.today().weekday() == 4:
    if True:

        cur_time = make_aware(datetime.datetime.now())
        print(cur_time)
        time_week_ago = (cur_time - datetime.timedelta(days=7))
        print(time_week_ago)
    # Query data within a week
        for usr in User.objects.all():
            print(usr)
            newsList=''
            posts = Post.objects.filter(time_create__range=(time_week_ago, cur_time))
            for each in posts:
                for cat in each.post_cat.all():
                    for usr2 in cat.subscribers.all():
                        if usr2==usr:
                            print(f'{usr} is subsribed on category {cat} post: {each.time_create} ')
                            print(datetime.datetime.today().weekday())
                            newsList+= str(f'{each.header}\n')
                            newsList+= str(f'{each.text}\n')
                            newsList+= str(f'категория {cat}\n\n\n')

                            #newsList+= str(f'\n<a href="127.0.0.1:8000/news/{each.pk}">гиперссылка</a>\n')

            if datetime.datetime.today().weekday() == 0:

                subject = 'Hello'
                from_email = 'vedavik@yandex.ru'
                to = usr.email
                html_content = render_to_string('news_week.html', {'posts': posts})
                text_content = 'News for week'
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                print (f'mail is sended to {usr.email}')



# функция, которая будет удалять неактуальные задачи
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
            trigger=CronTrigger(day_of_week="mon", hour="23", minute="15"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
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