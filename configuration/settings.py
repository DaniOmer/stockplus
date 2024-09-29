"""
Django settings for stockplus project.

Generated by 'django-admin startproject' using Django 3.1.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
from pathlib import Path
from decouple import config
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*').split()

# ENV = config('ENV', default="DEVELOPMENT") // Temporarily ignored
ENV="DEVELOPMENT"

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_ckeditor_5',
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

ROOT_URLCONF = 'configuration.urls'

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

WSGI_APPLICATION = 'configuration.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

if config('DATABASE') == "postgresql":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': config('DB_HOST'),
            'PORT': config('DB_PORT'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

"""
Project configuration
"""
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "templates/static"), ]
TEMPLATES[0]['DIRS'] = [os.path.join(BASE_DIR, 'templates/')]


"""
Logger
"""
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#         'builder': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }

"""
Ckeditor
"""
CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': [
            'heading', '|',
            'outdent', 'indent', 'Alignment', '|',
            'bold', 'italic', 'link', 'underline', 'strikethrough', 'code', 'subscript', 'superscript', 'highlight', '|',
            'bulletedList', 'numberedList', 'todoList', '|',
            'blockQuote', '|',
            'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', 'removeFormat', 'insertTable', ],
        'heading': {
            'options': [
                {'model': 'paragraph', 'title': 'Paragraph',
                    'class': 'ck-heading_paragraph'},
                {'model': 'heading1', 'view': 'h1', 'title': 'Heading 1',
                    'class': 'ck-heading_heading1'},
                {'model': 'heading2', 'view': 'h2', 'title': 'Heading 2',
                    'class': 'ck-heading_heading2'},
                {'model': 'heading3', 'view': 'h3',
                    'title': 'Heading 3', 'class': 'ck-heading_heading3'}
            ]
        }
    }
}

"""
SWAGGER UI configuration
"""
INSTALLED_APPS += ['drf_spectacular',]
SPECTACULAR_SETTINGS = {
    'TITLE': 'Stockplus',
    'DESCRIPTION': 'Inventory management application',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

"""
Builder configuration
"""
MIGRATION_MODULES = {'builder': 'stockplus.migrations.builder'}
AUTH_USER_MODEL = 'builder.User'
AUTHENTICATION_BACKENDS  = [
    'builder.auth.backends.EmailOrPhoneBackend',
    'django.contrib.auth.backends.ModelBackend',
]

INSTALLED_APPS += ["builder",] + [
    'builder.applications.user',
    'builder.applications.messenger',
    'builder.applications.company',
    'builder.applications.address',
    'builder.applications.subscription',
]

# Company configuration
USER_ROLE = [
    ('manager', 'Manager'),
    ('collaborator', 'Collaborator'),
    ('member', 'Member'),
]
USER_ROLE_DEFAULT = 'manager'
USER_ROLE_INVITE = 'collaborator'

"""
User permissions settings
"""
from stockplus.permissions import IsManager
INVITATION_PERMISSION = IsManager
ADDITIONAL_CRUD_PERMISSIONS = ['builder.applications.user.permissions.IsSelf', 'stockplus.permissions.IsManager']

# Subscription configuration
SUBSCRIPTION_MODEL = [
    ('stater', 'Starter'),
    ('premium', 'Premium'),
]

SUBSCRIPTION_PERMISSIONS = [
    ('stater', 'Starter Permissions'),
    ('premium', 'Premium Permissions'),
]


"""
SHOP Configuration settings
"""
INSTALLED_APPS += ['builder.applications.shop',]


"""
Stockplus configuration
"""
INSTALLED_APPS += [
    'stockplus',
    'stockplus.applications.pointofsale',
]


"""
## REST configuration
"""
INSTALLED_APPS += ['rest_framework',]
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ), 
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

"""
## Simple JWT Authentication
"""
seconds_delta = config('TOKEN_LIFETIME', default=86400, cast=int)
INSTALLED_APPS += ['rest_framework_simplejwt',]
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(seconds=seconds_delta),
    'REFRESH_TOKEN_LIFETIME': timedelta(seconds=seconds_delta),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_OBTAIN_SERIALIZER': 'builder.serializer.CustomTokenObtainPairSerializer',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(seconds=seconds_delta),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(seconds=seconds_delta),
}

EMAIL_VERIFICATION_TOKEN_LIFETIME = timedelta(seconds=seconds_delta)

"""
## Brevo (Sendinblue) - Mail and Sms service configuration
"""
SENDINBLUE_APIKEY = config("SENDINBLUE_APIKEY")

MISSIVE_SERVICE = config('MISSIVE_SERVICE', default=True)
MISSIVE_BACKENDS = 'builder.applications.messenger.backends'
MISSIVE_BACKEND_EMAIL = 'builder.applications.messenger.backends.email.sendinblue'
MESSENGER = {
    'sender_name': config('SENDER_NAME', default='contact'),
    'sender_email': config('SENDER_EMAIL', default='contact@stockplus.io'),
    'reply_name': config('REPLY_NAME', default='noreply'),
    'reply_email': config('REPLY_EMAIL', default='noreply@stockplus.io'),
}


"""
STRIPE Configuration
"""
STRIPE_API_KEY = config('STRIPE_API_KEY')


"""
## OAuth2 configuration
"""
INSTALLED_APPS += ['oauth2_provider',]

OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'groups': 'Access to your groups'}
}
# LOGIN_URL = '/admin/login/'


"""
Corsheaders configuration
"""
INSTALLED_APPS += ["corsheaders",]

MIDDLEWARE += [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

CORS_ALLOW_ALL_ORIGINS=True
# CORS_ALLOWED_ORIGINS = [
#     "https://stockplus.io",
#     "http://localhost:8080",
#     "http://127.0.0.1:3000",
# ]


"""
Frontend configuration
"""
FRONTEND_URL = config('FRONTEND_URL', default="http://stockplus.io")