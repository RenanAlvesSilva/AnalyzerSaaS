from django.contrib.auth.models import BaseUserManager

from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('O usuário precisa ter um e-mail')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, name, last_name, password, **extra_fields)



   