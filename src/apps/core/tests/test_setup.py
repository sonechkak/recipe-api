from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from .test_base import BaseTestCase


User = get_user_model()


class AdminSiteTests(BaseTestCase):
    def setUp(self):
        """Выполняется перед каждым тестом."""
        self.client = Client()  # создаем клиента
        self.admin_user = User.objects.create_superuser(
            email="test@appdev.com",
            password="test123"
        )
        self.client.force_login(self.admin_user)
        self.user = User.objects.create_user(
            email="test@app.com",
            password="test123",
            name="Test User Full Name"
        )

    def test_users_listed_on_user_page(self):
        """Пользователи отображаются в списке пользователей."""
        from django.urls import get_resolver
        print("Available URL patterns:")
        for pattern in get_resolver().reverse_dict.keys():
            if isinstance(pattern, str):
                print(pattern)

        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)
