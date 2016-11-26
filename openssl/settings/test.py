from openssl.settings.common import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    'SECRET_KEY', '3l1ax1(0u1e$^iavnx^a_y7w9ivr+rix*nr_w#tug#h($p5fmp')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/
HOST = 'openssl.dev'

INTERNAL_IPS = (
    '127.0.0.1',
)

ALLOWED_HOSTS = (
    '*',
)

THIRD_PARTY_APPS = (

    # tests
    'nose',

)

INSTALLED_APPS += THIRD_PARTY_APPS + COMMON_APPS


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'public/app/views'),
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DEFAULT_URL_SCHEME = 'http'
ALLOWED_HOSTS = ['*']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"


STATIC_ROOT = os.path.join(BASE_DIR, "tmp")
MEDIA_ROOT = os.path.join(BASE_DIR, "uploads")


STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "public/libs"),
    os.path.join(BASE_DIR, "public/app")
)

FILE_UPLOAD_HANDLERS = (
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
)

# STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'djangobower.finders.BowerFinder',
    # 'pipeline.finders.PipelineFinder',
)


# Running tests with django-nose
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Apps for nose coverage
NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=apps.api',
    '--cover-package=apps.domain',
    '--cover-package=apps.certificate',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'slack': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'slack.utils.SlackHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'slack'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

IS_SLACK_ENABLED = True
SLACK_TOKEN = '<token>'
SLACK_CHANNEL = '#<channel>'
SLACK_USERNAME = '<username>'

SLACK_PARAMS = {
    'GET': True,
    'POST': True,
    'META': {
        'SERVER_NAME': True,
        'HTTP_ACCEPT': True
    }
}
