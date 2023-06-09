"""
Django settings for devops_tools project.

Generated by 'django-admin startproject' using Django 4.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-1*t&^fhsf$h**qpzaom%41tf)g^^9!qnm9i@r_---z+%w4!p4d'


ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'apollo',
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

ROOT_URLCONF = 'devops_tools.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR.joinpath('templates')],
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

WSGI_APPLICATION = 'devops_tools.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/\#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# STATIC_ROOT = BASE_DIR.joinpath('static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (BASE_DIR.joinpath('static'),)

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/\#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# custom logger
BASE_LOG_DIR = BASE_DIR.joinpath('logs')
LOGGING = {
    # 版本，无需改动
    'version': 1,
    # 是否弃用已经存在的日志，True表示弃用，False表示不弃用
    'disable_existing_loggers': False,
    # 格式器
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]'
                      '[%(levelname)s][%(message)s]'
        },
        'standard': {
            'format': '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
        },
        'simple': {
            'format': '[%(levelname)s][ %(message)s]'
        },
    },
    # 过滤器
    'filters': {
    },
    # 处理器
    'handlers': {
        # 在终端打印
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        # 默认 INFO 级别日志
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',     # 保存到文件，自动切
            'filename': BASE_LOG_DIR.joinpath('app.log'),        # 日志文件位置
            'maxBytes': 1024 * 1024 * 50,                        # 日志大小 50M
            'backupCount': 3,                                    # 日志备份数量
            'formatter': 'standard',                             # 使用哪种日志格式
            'encoding': 'utf-8',                                 # 保存的格式
        },
        # 错误级别日志
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_LOG_DIR.joinpath('error.log'),
            'maxBytes': 1024 * 1024 * 50,
            'backupCount': 1,
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
    },
    # 日志器
    'loggers': {
        # 默认的logger应用如下配置
        'defaultlogger': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True,   # 不向更高级别的logger传递
        }
    }
}
