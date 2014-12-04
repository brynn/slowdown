"""
Django settings for slowdown project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 't*u7fa3xju42wdng9$h=-=#fz!r1&=u1cn8_+q2p*@!=a%!eaz'


ADMINS = (
    ('Brynn Shepherd', 'brynn.shepherd@gmail.com'),
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['.slowdown.io']

TIME_ZONE = 'America/New_York'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    'accounts',
    'south',
)


AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.twitter.TwitterOAuth',
    'social.backends.instagram.InstagramOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_PROFILE_MODULE = 'accounts.UserProfile'

SOCIAL_AUTH_FACEBOOK_KEY = '299858773498917'
SOCIAL_AUTH_FACEBOOK_SECRET = '2a551d1c2ce896799fd1900e9040be2a'

SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

SOCIAL_AUTH_TWITTER_KEY = 'iOPlmeF3uXxJdNvttvYWA'
SOCIAL_AUTH_TWITTER_SECRET = 'RkRkkTImAHaH247fj2s4VTIftdv3odYJ6c5Tu2Y'

SOCIAL_AUTH_INSTAGRAM_KEY = '60093b8d6bc94f3b8c6daa947c658985'
SOCIAL_AUTH_INSTAGRAM_SECRET = '9461c5c0759b442f80728b4b65296f83'

# TWITTER_ACCESS_TOKEN = '7019132-3DpATCGVeQPKIC16zJo01cf6ijmXaPSL97yqccDtZ4'
# TWITTER_ACCESS_TOKEN = 'QZQ8FBaspW74qfPnSJ4nFM0mxyRMOtB7SgKs2V5GHTaOa'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/signup/'
URL_PATH = ''
SOCIAL_AUTH_STRATEGY = 'social.strategies.django_strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social.apps.django_app.default.models.DjangoStorage'

# SOCIAL_AUTH_EMAIL_FORM_URL = '/signup-email'
SOCIAL_AUTH_EMAIL_FORM_HTML = 'email_signup.html'
SOCIAL_AUTH_EMAIL_VALIDATION_FUNCTION = 'accounts.mail.send_validation'
SOCIAL_AUTH_EMAIL_VALIDATION_URL = '/email-sent/'
# SOCIAL_AUTH_USERNAME_FORM_URL = '/signup-username'
SOCIAL_AUTH_USERNAME_FORM_HTML = 'username_signup.html'

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    #'accounts.pipeline.require_email',
    'social.pipeline.mail.mail_validation',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
    'accounts.models.social_auth_to_profile'
)

SOCIAL_AUTH_DISCONNECT_PIPELINE = (
    'social.pipeline.disconnect.get_entries',
    'social.pipeline.disconnect.revoke_tokens',
    'social.pipeline.disconnect.disconnect'
)

TEMPLATE_DIRS = (
	'/home/bshepherd/webapps/slowdown_django/slowdown/templates'
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'slowdown.urls'

WSGI_APPLICATION = 'slowdown.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'slowdown',                      
        'USER': 'bshepherd',                      
        'PASSWORD': 'ysJfRbzB',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = '/home/bshepherd/webapps/slowdown_static/'

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/home/bshepherd/webapps/slowdown_django/slowdown/static',
)

MEDIA_ROOT = '/home/bshepherd/webapps/slowdown_static/audio/'
MEDIA_URL = '/audio/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'slowdown'
EMAIL_HOST_PASSWORD = 'wschamps42'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'mysite.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers':['file'],
            'propagate': True,
            'level':'DEBUG',
        },
        'slowdown': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }
}

GEOIP_PATH = '/home/bshepherd/webapps/slowdown_django/slowdown/geoip'
#GEOIP_LIBRARY_PATH '/home/bshepherd/lib/libGeoIP.so'