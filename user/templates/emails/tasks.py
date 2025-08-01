from celery import shared_task
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from user.models import CostumerUser
from django.conf import settings
from django.template.loader import render_to_string

@shared_task
def send_user_token_email(user_id, action , link_path, subject, message_template):
    try:
        user = CostumerUser.objects.get(pk=user_id)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        link = f"http://127.0.0.1:8000/{link_path}/{uid}/{token}"
        message = render_to_string(message_template, {
          "user": user,
          "link": link,
          "action": action
        })
        send_mail(
          subject,
          message,
          settings.EMAIL_HOST_USER,
          [user.email],
          fail_silently=False,
        )
        return True
    except CostumerUser.DoesNotExist:
        return False