# Backend сайта "Мой город"

[![Build Status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2FKirillYabl%2FMyCityBackend%2Fbadge%3Fref%3Dmain&style=flat)](https://actions-badge.atrox.dev/KirillYabl/MyCityBackend/goto?ref=main)
[![Coverage Status](https://coveralls.io/repos/github/KirillYabl/MyCityBackend/badge.svg?branch=main)](https://coveralls.io/github/KirillYabl/MyCityBackend?branch=main)

"Мой город" - это квест-игра, который проводится ежегодно для жителей города Ставрополь.

При проведении есть несколько типов квестов, например пешие, для велосипедистов и для людей увлекающихся спортивным ориентированием.

Для участия в квесте люди собираются в команды от 2 до 5 человек.

## Цель проекта

Данный репозиторий - API для сайта "Мой город". Квест-игра имеет большую историю с 2005 года и сейчас организаторам потребовалось "осовременить" техническую часть, т.к. координировать мероприятие при текущем количестве участников становится затруднительно.

## Как запустить

Должны быть установлены следующие программы

1. Python 3.9+
2. Docker 20+
3. Docker compose 2+

В папке `./my_city/my_city` создать файл `.env` со следующим содержанием:

### .env:

```text
DJANGO_SECRET_KEY=REPLACE_ME
POSTGRES_DB_URL=postgres://USER_NAME:DB_PASSWORD@db:5432/DB_NAME
POSTGRES_NAME=DB_NAME
POSTGRES_PASSWORD=DB_PASSWORD
POSTGRES_USER=USER_NAME
POSTGRES_HOST=db
POSTGRES_PORT=5432
PGDATA=/var/lib/postgresql/data/pgdata
MIN_MEMBERS_IN_TEAM=2
MAX_MEMBERS_IN_TEAM=5
DJANGO_SETTINGS_MODULE=my_city.settings
DJANGO_ENV=development
MAX_MEMBERS_IN_TEAM=5
ALLOWED_HOSTS='127.0.0.1,0.0.0.0'
```

Запустить БД из корневой папки проекта:

```shell
docker-compose run --rm -d db # запуск
docker-compose stop db # остановка
```

Создать виртуальное окружение в корневой папке проекта

```shell
python -m venv venv
```

Установить зависимости

```shell
pip install -r dev-requirements.txt
```

Перейти в папку `my_city` и выполнить миграции

```shell
cd ./my_city
python manage.py migrate
```

## Заполнение БД тестовыми данными

Для наполнения БД тестовыми данными `fill_test_data`

```shell
python manage.py fill_test_data
```

Чтобы удалить тестовые данные, необходимо выполнить команду `drop_test_data`

```shell
python manage.py drop_test_data
```

## Как запустить

Выполнить команду из папки `my_city` относительно корневой папки проекта

```shell
python manage.py runserver
```

## Как запустить тесты

```shell
pytest
```

## Как запустить линтер

```shell
ruff check ./my_city
```

## Как отформатировать импорты

```shell
ruff --select I ./my_city --fix
```

## Как запустить, используя Docker

Заполнить `my_city/my_city/.env`, как описано [тут](#env)

Сбилдить:

```shell
make build
```

Запустить/остановить контейнеры:

```shell
make up # запуск
make down # остановка
```

Выполнить миграции:

```shell
make migrate
```

Заполнить/очистить БД тестовыми данными:

```shell
make fill_db # заполнение
make drop_test_db # очистка
```

Запустить тесты:

```shell
make tests
```

Запустить линтер:

```shell
make lint
```

Запустить isort(отформатирует импорты):

```shell
make isort
```

## Используемые технологии

1. Python
   - Django
   - DRF
   - pytest
2. Postgresql
3. Docker
4. Docker compose

## Другие репозитории и важные ссылки внутри проекта

1. [Группа квеста во "Вконтакте"](https://vk.com/mg_stv)
2. [Frontend](https://github.com/IVKrylova/routes-of-my-city)
