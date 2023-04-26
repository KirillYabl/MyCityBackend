from my_city.settings.components.common import INSTALLED_APPS, MIDDLEWARE

DEBUG = True

INSTALLED_APPS += (
    'debug_toolbar',
    'drf_yasg',
)

MIDDLEWARE += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)
