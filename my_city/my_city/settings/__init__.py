from split_settings.tools import include
from os import environ

DEVELOPMENT_ENV = 'development'

ENV = environ.get('DJANGO_ENV') or DEVELOPMENT_ENV

base_settings = [
    'components/common.py',
    'components/database.py',
    'components/drf.py',
    'components/templates.py',
    'components/auth.py',
    f'environments/{ENV}.py',
]


include(*base_settings)
