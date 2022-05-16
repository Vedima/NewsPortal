from django.db.models.signals import post_save
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import send_mail
from .models import Category


# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
@receiver(post_save, sender=Category)
def notify_managers_appointment(sender, instance, created, **kwargs):
    #if created:
    #subject = f'{instance.client_name} '
    #else:
        #subject = f'Appointment changed for {instance.client_name} {instance.date.strftime("%d %m %Y")}'

    # отправляем письмо
    send_mail(
        subject=f'jj',
        # имя клиента и дата записи будут в теме для удобства
        message='jjll',  # сообщение с кратким описанием проблемы
        from_email='vedavik@yandex.ru',  # здесь указываете почту, с которой будете отправлять (об этом попозже)
        recipient_list=['vedima07@rambler,ru']  # здесь список получателей. Например, секретарь, сам врач и т. д.
    )