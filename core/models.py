
import os
import uuid
from django.conf import settings

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import( 
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

def user_image_field(instance, filename):
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    return os.path.join('uploads', 'user', filename)


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email address")
    
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()

        return user
    
    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_supersuser = True
        user.save(using=self._db)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    cpf = models.CharField(max_length=255, null=False)
    url_imagem = models.ImageField(null=True, upload_to=user_image_field)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
class Conta(models.Model):
    agencia = models.CharField(max_length=4)
    numero = models.CharField(max_length=16)
    user = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(default=timezone.now)