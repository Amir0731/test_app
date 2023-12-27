import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-2wb!ixw!i&_#=y84-u2kxu1&&9!sk3d9c@ld&0b-wt1&-0h)4p'
DEBUG = False

# ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['.vercel.app', '.now.sh', '127.0.0.1', 'localhost']
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django.contrib.redirects',
    'modeltranslation',
    'django.contrib.admin',
    'monitoring',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "django.middleware.locale.LocaleMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.contrib.redirects.middleware.RedirectFallbackMiddleware'
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates'
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

WSGI_APPLICATION = 'config.wsgi.application'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'railway',
        'USER': 'postgres',
        'PASSWORD': '5ef*e4DecFB*b*5F4Fa4dE4FeADAGACF',
        'HOST': 'roundhouse.proxy.rlwy.net',
        'PORT': '48264'
    }
}

AUTH_USER_MODEL = 'monitoring.User'

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

# LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# STATIC_ROOT = BASE_DIR / 'staticfiles'
# STATICFILES_DIRS = [BASE_DIR / 'static']

LOGOUT_REDIRECT_URL = '/'

STATIC_URL = 'static/'
# STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = os.path.join(BASE_DIR, 'static'),
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media-files'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LANGUAGE_CODE = 'uz-uz'

LANGUAGES = [
    ("uz", _("O'zbekcha")),
    ("ru", _("Русский")),
    ('en', _('English')),
]

MODELTRANSLATION_DEFAULT_LANGUAGE = 'uz'
LOCALE_PATHS = BASE_DIR, 'locale'

LOGIN_REDIRECT_URL = '/'
# PASSWORD_CHANGE_REDIRECT_URL ='/'


# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'amiryandrima@yandex.ru'
EMAIL_HOST_PASSWORD = 'rbvirnyfxsfpfyqv'
EMAIL_USE_SSL = True

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER
EMAIL_ADMIN = EMAIL_HOST_USER

# vpkawpratoxruszn