# Backend сайта "Мой город"

"Мой город" - это квест-игра, который проводится ежегодно для жителей города Ставрополь.

При проведении есть несколько типов квестов, например пешие, для велосипедистов и для людей увлекающихся спортивным ориентированием.

Для участия в квесте люди собираются в команды от 2 до 5 человек.

## Цель проекта

Данный репозиторий - API для сайта "Мой город". Квест-игра имеет большую историю с 2005 года и сейчас организаторам потребовалось "осовременить" техническую часть, т.к. координировать мероприятие при текущем количестве участников становится затруднительно.

## Как установить

Должны быть установлены следующие программы
1. Python 3.9+
2. Docker 20+
3. Docker compose 2+

В папке `./my_city/my_city` создать файл `.env` со следующим содержанием:

```text
DJANGO_SECRET_KEY=REPLACE_ME
POSTGRES_DB_URL=postgres://USER_NAME:DB_PASSWORD@localhost:5432/DB_NAME
POSTGRES_DB=DB_NAME
POSTGRES_USER=USER_NAME
POSTGRES_PASSWORD=DB_PASSWORD
PGDATA=/var/lib/postgresql/data/pgdata
```

Запустить БД в отдельном окне терминала из корневой папки проекта
```shell
docker-compose up
```

В другом окне терминала создать виртуальное окружение в корневой папке проекта

```shell
python -m venv venv
```

Установить зависимости

```shell
pip install -r requirements.txt
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