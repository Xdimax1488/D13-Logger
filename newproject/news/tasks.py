from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.utils.timezone import localtime
from django.conf import settings
from .models import *


@shared_task
def mail_fo_new_post(email_subscribers, new_post, link, category):
    html_content = render_to_string('mailing_new_content.html',
                                    {
                                        'new_post': new_post, 'link': link, 'category': category
                                    })
    msg = EmailMultiAlternatives(
        subject=f'Появились обновления в категории на которую вы подписаны',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=email_subscribers,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    print(f'Письмо отправлено {email_subscribers}')


@shared_task
def send_mail_subscribe(category, email):
    send_mail(
        subject='здравсивуйте',
        # имя клиента и дата записи будут в теме для удобства
        message=f'Вы были подписаны на категорию {category}',  # сообщение с кратким описанием проблемы
        from_email=settings.DEFAULT_FROM_EMAIL,  # здесь указываете почту, с которой будете отправлять (об этом попозже)
        recipient_list=[email, ]  # здесь список получателей. Например, секретарь, сам врач и т. д.
    )
    print(f'send email to {email}')


@shared_task
def send_mail_unsubscribe(category, email):
    send_mail(
        subject='здравсивуйте',
        # имя клиента и дата записи будут в теме для удобства
        message=f'Вы были одписаны на категорию {category}',  # сообщение с кратким описанием проблемы
        from_email=settings.DEFAULT_FROM_EMAIL,  # здесь указываете почту, с которой будете отправлять (об этом попозже)
        recipient_list=[email, ]  # здесь список получателей. Например, секретарь, сам врач и т. д.
    )
    print(f'send email to {email}')


@shared_task
def wk_newsletter():
    print(f'Start{localtime()}')
    # Если день недели воскресенье
    if datetime.isoweekday(datetime.now()) == 1:
        # Высчитываем время 7 дней назад
        week = localtime() - timedelta(days=7)
        # По очереди берем каждую категорию, и делаем рассылку его подписчикам
        categories = Category.objects.all()
        for category in categories:
            # Берем всех подписчиков этой темы, и создаем список почтовых адресов
            subscribers = User.objects.filter(categorysubscribers__category=category)
            subscribers_emails = []
            for user in subscribers:
                subscribers_emails.append(user.email)
                # Достаем все новости этой категории за последние 7 дней
                post_list = Post.objects.filter(postcategory__category=category, date_create__gt=week)
                print(post_list)

                # HTML страница для мыло
                html_content = render_to_string('templates/weekly_newsletter.html',
                                                {'posts': post_list, 'category': category, })
                # Достаем
                # Собираем тело сообщения
                msg = EmailMultiAlternatives(
                    subject=f'Все новости за прошедшую неделю',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=subscribers_emails,
                )
                msg.attach_alternative(html_content, "text/html")  # добавляем html
                msg.send()  # отсылаем
                print('Рассылка успешна отправлена')
