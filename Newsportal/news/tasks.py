from datetime import datetime, timedelta

from celery import shared_task
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from .models import Post, Category


@shared_task
def send_notification(preview, pk, post_title, subscribers):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}',
        }
    )
    msg = EmailMultiAlternatives(
        subject=post_title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def weekly_news():
    today = datetime.now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(post_time__gte=last_week)
    categories = set(posts.values_list('category__cat_name', flat=True))
    print(categories)
    subscribers = set(Category.objects.filter(cat_name__in=categories).values_list('subscribers', flat=True))
    print('второй принт')
    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts
        }
    )
    msg = EmailMultiAlternatives(
        subject='Weekly news',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()
