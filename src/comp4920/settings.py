import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'l0ms4m0qxye-matbknpjt^nhwe5&k9!#if&w*=)k=7cwy^932k'

DEBUG = True

TEMPLATE_DEBUG = True

SITE_DOMAIN = 'localhost'
ROOT_URL = 'http://' + SITE_DOMAIN + ':9000'

ALLOWED_HOSTS = [SITE_DOMAIN]

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'polygons'
)

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

MIDDLEWARE_CLASSES = (
    'lockout.middleware.LockoutMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'comp4920.urls'

WSGI_APPLICATION = 'comp4920.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'polygons',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

LANGUAGE_CODE = 'en-AU'

TIME_ZONE = 'Australia/Sydney'

USE_I18N = True

USE_L10N = False
DATE_FORMAT = 'd-m-Y'

USE_TZ = True

STATIC_ROOT = ''
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# Django-Lockout
LOCKOUT_MAX_ATTEMPTS = 5
LOCKOUT_TIME = 600 #seconds
LOCKOUT_ENFORCEMENT_WINDOW = 300 #seconds
