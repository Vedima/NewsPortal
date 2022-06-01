import os
#В первую очередь мы импортируем библиотеку для взаимодействия с операционной системой и саму библиотеку Celery.
from celery import Celery
from celery.schedules import crontab

#Второй строчкой мы связываем настройки Django с настройками Celery через переменную окружения.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

#Далее мы создаем экземпляр приложения Celery и устанавливаем для него файл конфигурации.
app = Celery('NewsPaper')

#Мы также указываем пространство имен, чтобы Celery сам находил все необходимые настройки в settings.py.
app.config_from_object('django.conf:settings', namespace='CELERY')

#Последней строчкой мы указываем Celery автоматически искать задания в файлах tasks.py каждого приложения проекта.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'action_every_monday_8am': {
        # Довбавляем нужную задачу
        'task': 'NewsPortal.tasks.my_email',
        # Расписание выполнения задачи
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        #'args': (5, 5),
    },
}