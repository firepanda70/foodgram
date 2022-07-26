# Проект Foodgram
![main workflow](https://github.com/firepanda70/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

# Описание

Веб-приложение для хранения и создания рецептов различных блюд.
Зарегестрированные на сервисе пользователи могут добавлять понравившиеся рецепты в корзину покупок, после чего загружать с сайта полный спиосок необходимых для приготовления блюд ингредиентов.
Проект запускается в трех контейнерах, бля Базы данных, Бэкенда и Фронтенда. 

# Файл .env
Находится в директории /infa
Пример наполнения:

```
DJANGO_KEY=secret_key
ALLOWED_HOSTS=localhost,127.0.0.1
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

# Установка

Клонировать репозиторий:

```
git clone https://github.com/firepanda70/foodgram-project-react
```

Перейти в директорию:

```
cd foodgram-project-react/infra
```

Запустить docker-compose

```
docker-compose up --build
```

Запустить bash в котейнере:

```
docker exec -it <infra_web CONTAINER_ID> bash
```

Выполнить миграции:

```
python manage.py makemigrations
python manage.py migrate
```

Собрать статику проекта:

```
python manage.py collectstatic
```

Заполнить базу данных тестовыми данными:

```
python manage.py loaddata data/fixtures.json
```

Админка тестовых данных:
```
email: admin@admin.admin
username: admin
password: admin
```

Подробная документация API будет находиться после запуска проекта по эндпоинту api/docs/

# Технологии:
- Python 3 
- Django
- PostgreSQL
- Gunicorn
- Nginx
- Яндекс.Облако(Ubuntu 18.04)
- Docker
