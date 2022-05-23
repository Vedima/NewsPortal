from django.db.models.signals import m2m_changed
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import send_mail
from .models import Post


# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
@receiver(m2m_changed, sender=Post.post_cat.through)
def notify_managers_appointment(sender, instance, action, **kwargs):
    if action == 'post_add':
        for each in instance.post_cat.all():
            for usr in each.subscribers.all():
                # отправляем письмо
                send_mail(
                    subject=f'new post {instance.header}',
                    # имя клиента и дата записи будут в теме для удобства
                    message=f'new post text :  {instance.text[0:25]}',  # сообщение с кратким описанием проблемы
                    from_email='vedavik@yandex.ru',  # здесь указываете почту, с которой будете отправлять (об этом попозже)
                    recipient_list=[usr.email]  # здесь список пользователей, которые подписаны на категорию
                )