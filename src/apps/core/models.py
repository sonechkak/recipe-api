import uuid
import os
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.conf import settings
from django.db import models


def recipe_image_file_path(instance, filename):
    """Генерирует путь для сохранения изображения рецепта."""
    ext = filename.split('.')[-1]  # получение расширения файла
    filename = f'{uuid.uuid4()}.{ext}'  # генерация уникального имени файла
    return os.path.join('uploads/recipe/', filename)  # возвращает путь для сохранения файла


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Создает и возвращает нового пользователя."""
        if not email:
            raise ValueError('Email обязателен.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)  # хэширует пароль
        user.save(using=self._db)  # сохраняет в БД, используя текущую БД

        return user

    def create_superuser(self, email, password):
        """Создает и возвращает суперпользователя."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Кастомная модель пользователя, использует email в качестве уникального идентификатора вместо username."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'  # email в качестве уникального идентификатора

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Tag(models.Model):
    """Тег для рецепта."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Ingredient(models.Model):
    """Ингредиент для рецепта."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Recipe(models.Model):
    """Рецепт."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    ingredients = models.ManyToManyField('Ingredient')
    tags = models.ManyToManyField('Tag')
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title
