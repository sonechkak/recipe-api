from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import test, status
from rest_framework.test import APIClient

from core.models import Recipe, Ingredient, Tag
from recipe.serializers import RecipeSerializer, RecipeDeatilSerializer


User = get_user_model()
RECIPES_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):
    """Возвращает URL для детального представления рецепта."""
    return reverse('recipe:recipe-detail', args=[recipe_id])


def sample_tag(user, name="Main course"):
    """Создание и возврат образца тега."""
    return Tag.objects.create(user=user, name=name)


def sample_ingredient(user, name="Cinnamon"):
    """Создание и возврат образца ингредиента."""
    return Ingredient.objects.create(user=user, name=name)


def sample_recipe(user, **params):
    """Создание и возврат образца рецепта."""
    defaults = {
        'title': 'Sample recipe',
        'time_minutes': 10,
        'price': 5.00
    }
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)


class PublicRecipeAPITests(TestCase):
    """Тестирование публичного API рецептов."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Тест на доступность API без авторизации."""
        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, 401)

    def test_login_required(self):
        """Тест на доступность API без авторизации."""
        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, 401)


class PrivateRecipeAPITests(TestCase):
    """Тестирование приватного API рецептов."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            'test@appdev.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """Тест на получение списка рецептов."""

        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipes_limited_to_user(self):
        """Тест на получение рецептов для текущего пользователя."""
        user2 = User.objects.create_user(
            'other@appdev.com',
            'testpass'
        )
        sample_recipe(user=user2)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_view_recipe_detail(self):
        """Тест на просмотр детальной информации о рецепте."""
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))  # Добавление тега к рецепту
        recipe.ingredients.add(sample_ingredient(user=self.user))  # Добавление ингредиента к рецепту

        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDeatilSerializer(recipe)
        self.assertEqual(res.data, serializer.data)  # Сравнение данных рецепта с данными сериализатора
