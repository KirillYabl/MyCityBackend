from my_city.settings.components.common import MIDDLEWARE, INSTALLED_APPS

DEBUG = True

INSTALLED_APPS += (
    'debug_toolbar',
    'drf_yasg',
)

MIDDLEWARE += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)
