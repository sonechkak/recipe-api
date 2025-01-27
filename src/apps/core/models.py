from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Создает и возвращает нового пользователя"""
        if not email:
            raise ValueError('Email обязателен.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password) # хэширует пароль
        user.save(using=self._db) # сохраняет в БД, используя текущую БД

        return user

class User(AbstractBaseUser, PermissionsMixin):
    """Кастомная модель пользователя, использует email в качестве уникального идентификатора вместо username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email' # email в качестве уникального идентификатора

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
