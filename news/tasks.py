import datetime
from datetime import timedelta, datetime

from celery import shared_task
from project.celery import app
from celery.schedules import crontab

from django.core.mail import EmailMultiAlternatives

from news.models import Post, Category
from django.template.loader import render_to_string
from django.conf import settings


# отправка писем подписчикам с новой новостью в разделе

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




@shared_task
def notify_about_new_post(pk):
    post =Post.objects.get(pk=pk)
    categories = post.category.all()
    subscribers_emails = []

    for cat in categories:
        subscribers = cat.subscribers.all()
        subscribers_emails += [s.email for s in subscribers]

    send_notifications(post.preview(), post.pk, post.title, subscribers_emails)

# отправка еженедельных подборок
@shared_task
def my_job():
    today = datetime.now()
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



