import django_heroku
"""
Django settings for BaseProject project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
import django_heroku
import os
import pymongo , json 
from urllib.parse import (
    ParseResult, SplitResult, _coerce_args, _splitnetloc, _splitparams, quote,
    quote_plus, scheme_chars, unquote, unquote_plus,
    urlencode as original_urlencode, uses_params,
)
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '36=5gg7=wzwhpdr2vr&!5^jf2e$0#6@4e##=8ny#tj2#*6#dl('

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
    'django.contrib.humanize',
    'livesync',
    'django.contrib.staticfiles',
    'Users',
    'SmsBaseApp',
    'SmsBackEnd',
    'crispy_forms',
    'social_django',
    'rest_framework',
    'django_otp',
    'django_otp.plugins.otp_static',
    'django_otp.plugins.otp_totp',
    'two_factor',
    'Frontend'
    
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'livesync.core.middleware.DjangoLiveSyncMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    

]

DJANGO_LIVESYNC = {
    'PORT': 8000  # this is optional and is default set to 9001.
}

ROOT_URLCONF = 'BaseProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['Frontend/templates', 'Users/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'social_django.context_processors.backends',  # <--
                'social_django.context_processors.login_redirect', # <--
            ],
        },
    },
]

WSGI_APPLICATION = 'BaseProject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {

        'NAME': 'base_project_db',  # ชื่อฐานข้อมูล

        'ENGINE': 'django.db.backends.mysql',  # <- window
        # 'ENGINE': 'mysql.connector.django', #  <- linux
        'OPTIONS': {
            'sql_mode': 'traditional',
        },
        'USER': 'root',  # ชื่อผู้ใช้

        'PASSWORD': '',  # รหัสผ่าน12

        'HOST': '127.0.0.1',  # โฮมฐานข้อมูล

        'PORT': '3306',  # port ของโฮมฐานข้อมูล

        'SET': 'storage_engine=INNODB,character_set_connection=utf8,collation_connection=utf8_unicode_ci',

    }
}

MONGO_URL = '127.0.0.1'
MONGO_PORT = '27017'
MONGO_USER = 'user'
MONGO_PASSWORD = 'pass'
PLOTLY_SERVER_URL = ''
# CONNECTMONGO = pymongo.MongoClient(MONGO_URL, int(MONGO_PORT))
# endpoint_uri = "mongodb://%s:%s@%s:%s" % (quote_plus(MONGO_USER), quote_plus(MONGO_PASSWORD), MONGO_URL, int(MONGO_PORT))
# CONNECTMONGO = pymongo.MongoClient(endpoint_uri)pip install dnspython
CONNECTMONGO = pymongo.MongoClient('mongodb+srv://admin:1234@ricedna.sj3ht.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
# pio.orca.config.server_url = PLOTLY_SERVER_URL

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Bangkok'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATIC_URL = '/static/'
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "static"),
# ]
# LOGIN_URL = 'two_factor:login'
LOGIN_URL = '/Users/login/'
LOGIN_REDIRECT_URL = '/SmsBaseApp/home/'
LOGOUT_URL = '/Users/logout/'
LOGOUT_REDIRECT_URL = '/Users/login/'

DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': '/Users/athiphat/backup/'}
# CRON JOB
CRONJOBS = [
    # ('*/1 * * * *', 'django.core.management.call_command', ['dumpdata', 'auth'], {'indent': 4}, '> /Users/athiphat/backup/joe2.json'),
    ('* * * * *', 'SmsBackEnd.cron.my_scchuled_job_dbbackup', '>> /Users/athiphat/backup/file.log'),
    # ('*/2 * * * *', 'django.core.management.call_command', ['dumfpdata', 'auth'], {'indent': 4}, '> /Users/athiphat/backup/dump.json'),

]

CRON_CLASSES = [
    'SmsBackEnd.cron.MyCronJob',
    'SmsBackEnd.cron.MyCronJobAtTime',
    # ...
]

# Email protocol  
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = '' # email for 
EMAIL_HOST_PASSWORD = '' #pass 

EMAIL_PORT = 587


LINE_CHANNEL_ACCESS_TOKEN = ""
LINE_CHANNEL_SECRET = ""

SOCIAL_AUTH_FACEBOOK_KEY = "5119075804830533"        # App ID
SOCIAL_AUTH_FACEBOOK_SECRET = "1f5ac7bb431a06d363532753e392de52" 
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'user_link'] # add this
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {       # add this
  'fields': 'id, name, email, picture.type(large), link'
}
SOCIAL_AUTH_FACEBOOK_EXTRA_DATA = [                 # add this
    ('name', 'name'),
    ('email', 'email'),
    ('picture', 'picture'),
    ('link', 'profile_url'),
]

# Auth socail
AUTHENTICATION_BACKENDS = [
    'social_core.backends.linkedin.LinkedinOAuth2',
    'social_core.backends.instagram.InstagramOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

REST_FRAMEWORK = {
  'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
}

# at the bottom of settings.py
django_heroku.settings(locals())