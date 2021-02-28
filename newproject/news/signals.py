from django.db.models.signals import m2m_changed
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string  # импортируем функцию, которая срендерит наш html
from django.conf import settings
from .models import *
from .tasks import mail_fo_new_post


@receiver(m2m_changed, sender=Post.post_category.through)
def notify_new_post(sender, instance, **kwargs):
    if kwargs['action'] == "post_add":

        change_category = Category.objects.filter(postcategory__post=instance)
        if change_category.count() == 1:
            category = Category.objects.get(postcategory__post=instance)

            subscribers = User.objects.filter(categorysubscribers__category=category)
            email_subscribers = []
            for email in subscribers:
                email_subscribers.append(email.email)
            print(email_subscribers)

            new_post = f'{instance.text_title}'
            link = f'{Post.objects.get(postcategory__post=instance).id}'
            category = f'{category}'

            mail_fo_new_post.apply_async([email_subscribers, new_post, link, category], countdown=10)
