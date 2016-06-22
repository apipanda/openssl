from openssl.settings.common import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    'SECRET_KEY', '3l1ax1(0u1e$^iavnx^a_y7w9ivr+rix*nr_w#tug#h($p5fmp')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/
HOST = 'openssl.io'

INTERNAL_IPS = (
    '127.0.0.1',
)

ALLOWED_HOSTS = (
    '.openssl.io',
)

THIRD_PARTY_APPS = (
    'storages',
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

DEFAULT_URL_SCHEME = 'https'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.getenv('DB_HOST'),
        'NAME': os.getenv('DB_NAME'),
        'PORT': os.getenv('DB_PORT'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASS')
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
DEFAULT_FILE_STORAGE = 'libs.storages.S3Storage.S3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
