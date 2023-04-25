import dj_database_url

from my_city.settings.env import environ_env

POSTGRES_DB_URL = environ_env.str('POSTGRES_DB_URL')

DATABASES = {'default': dj_database_url.config(default=POSTGRES_DB_URL)}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
