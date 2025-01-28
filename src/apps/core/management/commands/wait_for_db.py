import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management import BaseCommand


class Command(BaseCommand):
    """Django команда для ожидания доступности базы данных."""

    def handle(self, *args, **options):
        self.stdout.write("Ожидание базы данных...")
        db_conn = None
        while not db_conn:  # Пока не установлено соединение с базой данных
            try:
                db_conn = connections["default"]  # Подключение к базе данных по умолчанию
            except OperationalError:
                self.stdout.write("База данных недоступна, ожидание 1 секунду...")  # Вывод сообщения в консоль
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("База данных доступна!"))
