import os
import tempfile

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from PIL import Image
from rest_framework import test, status
from rest_framework.test import APIClient

from core.models import Recipe, Ingredient, Tag
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer


User = get_user_model()
RECIPES_URL = reverse('recipe:recipe-list')

def image_upload_url(recipe_id):
    """Возвращает URL для загрузки изображения рецепта."""
    return reverse('recipe:recipe-upload-image', args=[recipe_id])


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

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)  # Сравнение данных рецепта с данными сериализатора

    def test_create_basic_recipe(self):
        """Тест на создание рецепта."""
        payload = {
            'title': 'Шоколадный чизкейк',
            'time_minutes': 30,
            'price': 5.00
        }
        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])

        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe, key))

    def test_create_recipe_with_tags(self):
        """Тест на создание рецепта с тегами."""
        tag1 = sample_tag(user=self.user, name='Веган')
        tag2 = sample_tag(user=self.user, name='Дессерт')
        payload = {
            'title': 'Лаймовый чизкейк с авокадо',
            'tags': [tag1.id, tag2.id],
            'time_minutes': 60,
            'price': 20.00
        }
        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])

    def test_partial_update_recipe(self):
        """Тест на обновление рецепта."""
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        new_tag = sample_tag(user=self.user, name='Карри')
        payload = {
            'title': 'Курица карри',
            'tags': [new_tag.id]
        }
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload)

        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])  # Сравнение названия рецепта

        tags = recipe.tags.all()
        self.assertEqual(len(tags), 1)  # Проверка на количество тегов
        self.assertIn(new_tag, tags)  # Проверка на наличие нового тега

    def test_full_update_recipe(self):
        """Тест на полное обновление рецепта."""
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        payload = {
            'title': 'Спагетти карбонара',
            'time_minutes': 25,
            'price': 15.00
        }
        url = detail_url(recipe.id)
        res = self.client.put(url, payload)

        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.time_minutes, payload['time_minutes'])
        self.assertEqual(recipe.price, payload['price'])

        tags = recipe.tags.all()
        self.assertEqual(len(tags), 0)


class RecipeImageUploadTests(TestCase):
    """Тестирование загрузки изображений рецептов."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            'user',
            'testpass',
        )
        self.client.force_authenticate(self.user)  # Авторизация пользователя
        self.recipe = sample_recipe(user=self.user)  # Создание образца рецепта

    def tearDown(self):
        self.recipe.image.delete()  # Удаление изображения

    def test_upload_image_to_recipe(self):
        """Тест на загрузку изображения к рецепту."""
        url = image_upload_url(self.recipe.id)  # Получение URL для загрузки изображения
        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = Image.new('RGB', (10, 10))  # Создание изображения
            img.save(ntf, format='JPEG')  # Сохранение изображения
            ntf.seek(0)
            res = self.client.post(url, {'image': ntf}, format='multipart')  # Загрузка изображения

        self.recipe.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.recipe.image.path))  # Проверка на наличие изображения

    def test_upload_image_bad_request(self):
        """Тест на загрузку недопустимого изображения."""
        url = image_upload_url(self.recipe.id)
        res = self.client.post(url, {'image': 'notimage'}, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_recipes_by_tags(self):
        """Тест """
