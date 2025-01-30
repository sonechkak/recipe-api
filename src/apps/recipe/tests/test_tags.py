from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag
from recipe.serializers import TagSerializer

User = get_user_model()
TAGS_URL = reverse('recipe:tag-list')


class PublicTagsAPITests(TestCase):
    """Тест на доступность тегов для неавторизованного пользователя."""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Тест на недоступность API без авторизации."""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsAPITests(TestCase):
    """Тест на доступность тегов для авторизованного пользователя."""

    def setUp(self):
        self.user = User.objects.create_user(
            'test@devapp.com',
            'password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)  # авторизация

    def test_retrieve_tags(self):
        """Тест на получение списка тегов."""
        Tag.objects.create(user=self.user, name='Вегетарианское')
        Tag.objects.create(user=self.user, name='Десерт')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('name')
        serializer = TagSerializer(tags, many=True)  # many=True для сериализации списка

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)  # сравнение сериализованных данных

    def test_tags_limited_to_user(self):
        """Тест на получение тегов только для текущего пользователя."""
        user2 = User.objects.create_user(
            'other@appdev.com',
            'testpass'
        )
        Tag.objects.create(user=user2, name='Фрукты')
        tag = Tag.objects.create(user=self.user, name='Компот')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)  # проверка количества тегов
        self.assertEqual(res.data[0]['name'], tag.name)  # проверка имени тега
