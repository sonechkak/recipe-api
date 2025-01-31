from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient
from recipe.serializers import IngredientSerializer

User = get_user_model()
INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientsApiTests(TestCase):
    """Тест на доступность ингредиентов для неавторизованного пользователя."""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Тест на недоступность API без авторизации."""
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
    """Тест на доступность ингредиентов для авторизованного пользователя."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            'test@appdev.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients_list(self):
        """Тест на получение списка ингредиентов."""
        Ingredient.objects.create(user=self.user, name='Капуста')
        Ingredient.objects.create(user=self.user, name='Соль')

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('name')
        serializer = IngredientSerializer(ingredients, many=True)  # many=True для сериализации списка
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Тест на получение ингредиентов только для текущего пользователя."""
        user2 = User.objects.create_user(
            'other@appdev.com',
            'testpass'
        )
        Ingredient.objects.create(user=user2, name='Масло')  # ингредиент для другого пользователя
        ingredient = Ingredient.objects.create(user=self.user, name='Сахар')  # ингредиент для текущего пользователя

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)