"""
Django settings for {{cookiecutter.__project_slug}} project.

Generated by 'django-admin startproject' using Django 4.1

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import datetime
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from configurations import Configuration, values


class Base(Configuration):
    BASE_DIR = Path(__file__).resolve().parent.parent

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = values.Value('{{ random_ascii_string(50) }}')

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    ALLOWED_HOSTS = values.ListValue([])  # Would be passed from above in the ecs task
    CORS_ALLOWED_ORIGINS = values.ListValue([])
    CSRF_TRUSTED_ORIGINS = values.ListValue([])  # for where you're running in a container and need the admin
    # Application definition
    THIRD_PARTY_APPS = [
        'corsheaders',
        'rest_framework_simplejwt',
        'rest_framework',
        'django_extensions',
        'import_export',
        'drf_spectacular'
    ]
    DJANGO_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ]
    {{cookiecutter.project_name|replace('-','_')|upper}}_APPS = []
    INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + {{cookiecutter.project_name|replace('-','_')|upper}}_APPS

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.LoginRequiredMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        "{{cookiecutter.__project_slug}}.middleware.TimezoneMiddleware",
        'querycount.middleware.QueryCountMiddleware'

    ]
    QUERYCOUNT = {
        'THRESHOLDS': {
            'MEDIUM': 50,
            'HIGH': 200,
            'MIN_TIME_TO_LOG': 0,
            'MIN_QUERY_COUNT_TO_LOG': 5
        },
        'IGNORE_REQUEST_PATTERNS': [],
        'IGNORE_SQL_PATTERNS': [],
        'DISPLAY_DUPLICATES': None,
        'RESPONSE_HEADER': None
    }

    ROOT_URLCONF = "{{cookiecutter.__project_slug}}.urls"

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
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

    WSGI_APPLICATION = "{{cookiecutter.__project_slug}}.wsgi.application"

    # Database
    # https://docs.djangoproject.com/en/4.1/ref/settings/#databases

    DATABASES = values.DatabaseURLValue("postgresql://{{cookiecutter.__project_slug}}_user:{{cookiecutter.__project_slug}}_pass@127.0.0.1:5432/{{cookiecutter.__project_slug}}_db")

    # Password validation
    # https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

    REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework_simplejwt.authentication.JWTAuthentication',
        ),
        'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
        'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
            'rest_framework.renderers.BrowsableAPIRenderer'
        ),
        'PAGE_SIZE': 30
    }

    SIMPLE_JWT = {
        # Consider customizing other stuff here: https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html
        "ACCESS_TOKEN_LIFETIME": datetime.timedelta(days=30)
    }

    # Internationalization
    # https://docs.djangoproject.com/en/4.1/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    USER_TZ = values.Value()

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/4.1/howto/static-files/
    STATIC_ROOT = BASE_DIR / 'static'
    STATIC_URL = '/static/'

    STORAGES = {
        "default":
            {"BACKEND": 'storages.backends.s3boto3.S3Boto3Storage'},
        "staticfiles":
            {"BACKEND": 'django.contrib.staticfiles.storage.StaticFilesStorage'}

    }
    MEDIA_ROOT = values.Value(BASE_DIR / 'media')
    MEDIA_URL = '/media/'

    # Default primary key field type
    # https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field
    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


class Development(Base):
    CORS_ALLOW_ALL_ORIGINS = True
    ALLOWED_HOSTS = values.ListValue(["web", "localhost", "127.0.0.1"])

    CSRF_TRUSTED_ORIGINS = values.ListValue(["https://*.127.0.0.1"])
    STORAGES = {
        "default":
            {"BACKEND": 'django.core.files.storage.FileSystemStorage'},
        "staticfiles":
            {"BACKEND": 'django.contrib.staticfiles.storage.StaticFilesStorage'}

    }

class Testing(Development):
    PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ]
    DATABASES = values.DatabaseURLValue( # This is about defaulting to running vs docker db if you don't specify something else
        "postgresql://{{cookiecutter.__project_slug}}_user:{{cookiecutter.__project_slug}}_pass@127.0.0.1:5433/{{cookiecutter.__project_slug}}_db")

    STORAGES = {
        "default":
            {"BACKEND": 'django.core.files.storage.InMemoryStorage'},
        "staticfiles":
            {"BACKEND": 'django.contrib.staticfiles.storage.StaticFilesStorage'}

    }

class Staging(Base):
    DEBUG = False
    CORS_ALLOW_ALL_ORIGINS = False
    AWS_STORAGE_BUCKET_NAME = values.Value(environ_name="S3_STORAGE")


class Production(Base):
    DEBUG = False
    CORS_ALLOW_ALL_ORIGINS = False
    AWS_STORAGE_BUCKET_NAME = values.Value(environ_name="S3_STORAGE")
    # If heroku Add buckateer for s3 intergration

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        {%- if cookiecutter.heroku_app_name|length %}
        'whitenoise.middleware.WhiteNoiseMiddleware',
        {%- endif %}
        'django.contrib.sessions.middleware.SessionMiddleware',
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.LoginRequiredMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        "{{cookiecutter.__project_slug}}.middleware.TimezoneMiddleware",
        'querycount.middleware.QueryCountMiddleware'

    ]
