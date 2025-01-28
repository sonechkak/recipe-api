# Recipe API

API сервис для работы с рецептами, построенный на Django REST Framework.

## Описание

Recipe API - это RESTful сервис, который позволяет пользователям создавать, хранить и управлять кулинарными рецептами. API предоставляет возможности для добавления, редактирования, удаления и поиска рецептов, а также работы с ингредиентами и категориями блюд.

## Технологический стек

- Python 3.8+
- Django 4.2
- Django REST Framework 3.14
- PostgreSQL
- Docker
- Docker Compose

## Установка и запуск

### Предварительные требования

- Docker
- Docker Compose
- Git

### Шаги по установке

1. Клонируйте репозиторий:
```bash
git clone https://github.com/sonechkak/recipe-api.git
cd recipe-api
```

2. Создайте файл .env в корневой директории проекта и настройте переменные окружения:
```bash
DEBUG=1
SECRET_KEY=your-secret-key
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=recipe_db
SQL_USER=recipe_user
SQL_PASSWORD=recipe_password
SQL_HOST=db
SQL_PORT=5432
```

3. Запустите проект через Docker Compose:
```bash
docker compose up --build --force-recreate
```

4. Примените миграции:
```bash
docker compose exec web python src/manage.py migrate
```

5. Создайте суперпользователя (опционально):
```bash
docker compose exec web python src/manage.py createsuperuser
```

Приложение будет доступно по адресу: http://127.0.0.1:8000

## Документация API

Подробная документация API доступна по следующим адресам:
- Swagger UI: `/api/schema/swagger-ui/`
- ReDoc: `/api/schema/redoc/`

## Тестирование

Для запуска тестов используйте команду:
```bash
 docker compose exec web sh -c "python src/manage.py test tests && flake8"
```

## Лицензия

Этот проект лицензирован под MIT License - смотрите файл [LICENSE](LICENSE) для подробностей.

## Поддержка

Если у вас возникли проблемы или есть предложения по улучшению проекта, пожалуйста, создайте issue в репозитории проекта.
