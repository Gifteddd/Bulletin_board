from celery import shared_task
from datetime import timezone, timedelta
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import *


@shared_task
def comment_send_email(comment_id):
    comment = Comment.objects.get(id=comment_id)
    send_mail(
        subject=f'Вас приветствует древо ММОRPG, где появились новые отклики! ',
        message=f'Уважаемый {comment.ad.author} ,ваши труды оценили, узнайте кто это!\n'
                f' Жми сюда: http://127.0.0.1:8000/comments/{comment.ad.id}',
        from_email='zhdankin.1981@yandex.ru',
        recipient_list=[comment.ad.author.email, ],
    )


@shared_task
def accept_email(response_id):
    comment = Comment.objects.get(id=response_id)
    print(comment.ad.author.email)
    send_mail(
        subject=f'Вас приветствует древо ММОRPG, мы передали ваше послание!',
        message=f'Уважаемый гость {comment.author} Ваш поклонник {comment.ad.author} принял ваше пожелание!\n'
                f'Узрите кто принимают ваши послания: http://127.0.0.1:8000/comments',
        from_email='zhdankin.1981@yandex.ru',
        recipient_list=[comment.author.email, ]
    )


@shared_task
def send_mail_monday_8am():
    now = timezone.now()
    list_week_adverts = list(Advertisements.objects.filter(created_at__gte=now - timedelta(days=7)))
    if list_week_adverts:
        for user in User.objects.filter():
            print(user)
            list_adverts = ''
            for advertisements in list_week_adverts:
                list_adverts += f'\n{advertisements.title}\nhttp://127.0.0.1:8000/advert/{advertisements.id}'
            send_mail(
                subject=f'Доска объявлений MMORPG: объявления за прошедшую неделю.',
                message=f'Доброго дня, {user.username}!\nПредлагаем Вам ознакомиться с новыми объявлениями, '
                        f'появившимися за последние 7 дней:\n{list_adverts}',
                from_email='',
                recipient_list=[user.email, ],
            )

