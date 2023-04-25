from my_city.settings.components import BASE_DIR, environ_env

SECRET_KEY = environ_env.str('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = environ_env.list('ALLOWED_HOSTS', ['127.0.0.1', '0.0.0.0'])

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user_app',
    'quest_app',
    'rest_framework',
    'django_filters',
    'sorl.thumbnail',
    'django_cleanup.apps.CleanupConfig',
    'knox',
    'dbbackup',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'my_city.urls'

WSGI_APPLICATION = 'my_city.wsgi.application'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_ROOT = BASE_DIR / 'media'
STATICFILES_DIRS = ((BASE_DIR / 'static'),)

# work_ip
INTERNAL_IPS = [
    '127.0.0.1',
]

MIN_MEMBERS_IN_TEAM = environ_env.int('MIN_MEMBERS_IN_TEAM', 2)
MAX_MEMBERS_IN_TEAM = environ_env.int('MAX_MEMBERS_IN_TEAM', 5)
