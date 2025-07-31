from celery import shared_task
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from user.models import CostumerUser
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status

@shared_task
def send_confirm_email(user_id):
    try:
        user = CostumerUser.objects.get(pk=user_id)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activate_link = f"http://localhost:3000/activate/{uid}/{token}"
        subject = "Confirmação de Conta"
        message = f"Para confirmar a sua conta, clique no link a seguir: {activate_link}"
        send_mail(
          subject,
          message,
          settings.EMAIL_HOST_USER,
          [user.email],
          fail_silently=False,
        )
        return Response({"message": "Email enviado com sucesso!"}, status=status.HTTP_200_OK)
    except CostumerUser.DoesNotExist:
        return Response({"error": "Usuário não encontrado"}, status=status.HTTP_404_NOT_FOUND)