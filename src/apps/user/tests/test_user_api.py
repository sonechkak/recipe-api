from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()
CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    """Вспомогательная функция для создания пользователя."""
    return User.objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Тестирование публичного API для пользователей."""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Тестирование создания пользователя с правильными данными."""
        payload = {
            'email': 'test@appdev.com',
            'password': 'testpass',
            'name': 'Test Name'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)  # Проверка статуса ответа.

        user = User.objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))  # Проверка пароля.
        self.assertNotIn('password', res.data)  # Проверка, что пароль не возвращается в ответе.

    def test_user_exists(self):
        """Тестирование создания пользователя, который уже существует."""
        payload = {
            'email': 'test@appdev.com',
            'password': 'testpass',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)  # Проверка статуса ответа.

    def test_password_too_short(self):
        """Тестирование создания пользователя с коротким паролем менее 5 букв."""
        payload = {
            'email': 'test@appdev.com',
            'password': 'pw',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)  # Проверка статуса ответа.
        user_exists = User.objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exists)  # Проверка, что пользователя не существует.

    def test_create_token_for_user(self):
        """Тест на создание токена для пользователя."""
        payload = {
            'email': 'test@appdev.com',
            'password': 'testpass',
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Тест на создание токена с невалидными данными."""
        create_user(email='test@appdev.com', password='testpass')
        payload = {
            'email': 'test@appdev.com',
            'password': 'wrong',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Тест на создание токена, если пользователя не существует."""
        payload = {
            'email': 'test@appdev.com',
            'password': 'wrong',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Тест на строгость полей email и password."""
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
