from datetime import datetime, timedelta

from celery import shared_task
from project.celery import app
from celery.schedules import crontab
# import time
# from .models import Category
# @shared_task
# def hello():
#     time.sleep(2)
#     print("Hello, world!")

from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from news.models import PostCategory, Post, Category
from django.template.loader import render_to_string
from django.conf import settings


# отправка писем подписчикам с новой новостью в разделе
@shared_task
def send_notifications(preview, pk, title, subscribers):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content,'text/html')
    msg.send()




@receiver(m2m_changed,sender =PostCategory)
def notify_about_new_post(sender,instance,**kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subscribers_emails = []

        for cat in categories:
            subscribers = cat.subscribers.all()
            subscribers_emails += [s.email for s in subscribers]

        send_notifications.delay(instance.preview(), instance.pk, instance.title, subscribers_emails)

# отправка еженедельных подборок
@shared_task
def my_job():
    today=datetime.datetime.now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(time_in__gte=last_week)
    categories = set(posts.values_list('category__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))
    html_content = render_to_string(
        'daily_post.html',
        {'link':settings.SITE_URL,
                'posts': posts,
                 }
            )
    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to = subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


app.conf.beat_schedule = {
    'weekly_news_subscribe': {
        'task': 'my_job',
        'schedule': crontab(hour=10, minute=52, day_of_week='wednesday'),
    },
}

