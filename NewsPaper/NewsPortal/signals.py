from django.db.models.signals import m2m_changed
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import send_mail
from .models import Post
from .tasks import send_email_add_news


# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
@receiver(m2m_changed, sender=Post.post_cat.through)
def notify_managers_appointment(sender, instance, action, **kwargs):
    # Если тип изменения было добавление, то...
    if action == 'post_add':
         for each in instance.post_cat.all():
             for usr in each.subscribers.all():
                 user = usr.email
                 title = instance.header
                 text = instance.text[0:25]
                 send_email_add_news.delay(title, text, user)
        #         # отправляем письмо
        #         send_mail(
        #             subject=f'new post {instance.header}',
        #             message=f'new post text :  {instance.text[0:25]}',  # сообщение с кратким описанием проблемы
        #             from_email='vedavik@yandex.ru',  # здесь указываете почту, с которой будете отправлять (об этом попозже)
        #             recipient_list=[usr.email]  # здесь список пользователей, которые подписаны на категорию
        #         )