# Проект Foodgram
![main workflow](https://github.com/firepanda70/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

# Описание

Веб-приложение для хранения, создания рецептов, с возможностью подписываться на авторов,
добавлять рецепты в избранное и выгружать список необходимых ингредиентов для покупки

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

### Пример развернутого проекта на сервере:
http://84.201.178.124/

### Документация API:
http://84.201.178.124/api/docs/

### Админка:
http://84.201.178.124/admin/
