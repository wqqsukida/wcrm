"""
Django settings for wcrm project.

Generated by 'django-admin startproject' using Django 1.11.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9s4^6)n=h*v(b1ay71gj$0ihqny#fgb_+!dh)b8m)w5g3vhm&@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rbac.apps.RbacConfig',
    'arya.apps.AryaConfig',
    'crm.apps.CrmConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'rbac.middlewares.rbac.RbacMiddleware',
]

ROOT_URLCONF = 'wcrm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',  # jinja2模版
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),  # 模版文件位置
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'environment': 'wcrm.jinja2_env.environment',  # XXX为你的app名称,
        },
    },
]

WSGI_APPLICATION = 'wcrm.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR,'static'),
)


# ########################### 权限管理相关 ###########################3
PERMISSION_MENU_KEY = "asdkjalsdf9uajsdf"
PERMISSION_URL_DICT_KEY = "iujmsufnsdflsdkf"

VALID_URL= [
    '^/login/',
    '^/index/',
    '^/index_v3/',
    '^/403/',
    '^/logout/',
    '^/userinfo/',
    '^/get_cert_detail/',
    '^/dnspod/',
    '^/dnspod/add_domain/',
    '^/dnspod/del_domain/',
    '^/dnspod/domain_status',
    '^/dnspod/domain_log',
    '^/dnspod/domain_searchenginepush',
    '^/dnspod/domain_remark',
    '^/dnspod/domain_lock',
    '^/dnspod/domain_changegroup',
    '^/dnspod/domain_addgroup',
    '^/dnspod/domain_modgroup',
    '^/dnspod/domain_delgroup',
    '^/dnspod_record/',
    '^/dnspod_d/',
    '^/dnspod_d/gethistory_monitor/',
]

#===============falcon-api====================

user = 'root'
sig = '5dfd815de3ce11e7b107000c298269bc'
domain = 'http://192.168.67.129:8080'