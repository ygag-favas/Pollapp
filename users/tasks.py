from celery import Celery
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from kombu.utils import json
from .tokens import account_activation_token

User = get_user_model()

app = Celery('mysite.tasks', broker='redis://127.0.0.1:6379')


@app.task(serialiser='json')
def sent_activation_mail(user_id, context):
    user = User.objects.get(id=user_id)
    mail_subject = 'Activate your account.'
    context.update(
        {'user': user,
         'uid': urlsafe_base64_encode(
             force_bytes(user.pk)),
         'token': account_activation_token.make_token(
             user),
         })
    message = (render_to_string
               ('account/acc_active_email.html', context))
    to_email = user.email
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()
