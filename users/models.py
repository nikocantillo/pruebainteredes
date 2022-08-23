from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """crea y guarda un nuevo usuario"""

        if not email:
            raise ValueError('Usuarios deben tener siempre un correo')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """crea super usruario"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    """modelos personalizad de usuario login con eail"""
    email = models.EmailField(max_length=255, umnique=True)
    user_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Enterprise(models.Model):
    """modelos de empresas"""

    name = models.CharField(max_length=100, unique=True)
    adress = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=12)
    user= models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Empresa"
