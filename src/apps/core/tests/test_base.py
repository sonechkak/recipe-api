import os
import django

# Настраиваем Django только если он еще не настроен
if not os.environ.get('DJANGO_SETTINGS_MODULE'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()


from django.test import TestCase


class BaseTestCase(TestCase):
    pass
