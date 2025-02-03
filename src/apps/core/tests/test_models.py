from unittest.mock import patch
from django.contrib.auth import get_user_model

from core import models
from .test_base import BaseTestCase


User = get_user_model()


def sample_user(email="test@appdev.com", password="testpass"):
    """Создание простого пользователя."""
    return User.objects.create_user(email, password)


class ModelTests(BaseTestCase):
    def test_create_user_with_email_successful(self):
        """Тест создания пользователя с email."""
        email = 'test@app.com'
        password = 'testpass123'
        user = User.objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Тест нормализации email."""
        email = 'test@APP.COM'
        user = User.objects.create_user(email, 'testpass123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Тест создания пользователя с некорректным email."""
        with self.assertRaises(ValueError):
            User.objects.create_user(None, 'testpass123')

    def test_create_new_superuser(self):
        """Тест создания суперпользователя."""
        user = User.objects.create_superuser(
            'test@appdev.com',
            'testpass123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Тестирование тега."""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Тестирование ингредиента."""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)  # сравнение строк

    def test_recipe_str(self):
        """Тестирование рецепта."""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Стейк со сливочным соусом',
            time_minutes=5,
            price=5.00
        )

        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Тестирование генерации имени файла в корректной директории."""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid  # подмена uuid
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')
        exp_path = f'uploads/recipe/{uuid}.jpg'

        self.assertEqual(file_path, exp_path)
