from split_settings.tools import include

from my_city.settings.env import environ_env

DEVELOPMENT_ENV = 'development'
PRODUCTION_ENV = 'production'

ENV = environ_env.str('DJANGO_ENV')

if ENV is None:
    raise ValueError('DJANGO_ENV environment variable is not set"')

base_settings = [
    'components/common.py',
    'components/database.py',
    'components/drf.py',
    'components/templates.py',
    'components/auth.py',
    f'environments/{ENV}.py',
]


include(*base_settings)
