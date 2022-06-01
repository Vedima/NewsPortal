from celery import shared_task
import time
import datetime
from .models import Post, User
from django.utils.timezone import make_aware
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.mail import send_mail

@shared_task
# наша задача по рассылке писем
def my_email():
    print('a')
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

# Функция для асинхронной отправки емейл сообщения при добавления новости
@shared_task
def send_email_add_news(title, text, user):
            # отправляем письмо
    send_mail(
        subject=f'new post {title}',
        message=f'new post text :  {text}',  # сообщение с кратким описанием проблемы
        from_email='vedavik@yandex.ru',  # здесь указываете почту, с которой будете отправлять (об этом попозже)
        recipient_list=[user]  # здесь список пользователей, которые подписаны на категорию
    )
    print (f'mail is sended to {user}')