import os

import django
from django.test import TestCase
from django.contrib.auth import get_user_model

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.config.settings")
django.setup()

User = get_user_model()


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Тест создания пользователя с email."""
        email = "test@app.com"
        password = "testpass123"
        user = User.objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Тест нормализации email."""
        email = "test@APP.COM"
        user = User.objects.create_user(email, "testpass123")

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Тест создания пользователя с некорректным email."""
        with self.assertRaises(ValueError):
            User.objects.create_user(None, "testpass123")

    def test_create_new_superuser(self):
        """Тест создания суперпользователя."""
        user = User.objects.create_superuser(
            "test@appdev.com",
            "testpass123"
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
