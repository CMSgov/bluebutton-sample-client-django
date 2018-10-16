"""
Django settings for bbc project.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

from django.contrib.messages import constants as messages

from .utils import bool_env

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.join(BASE_DIR, '..')


__author__ = "Alan Viars"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'piehme*+^#hylq8uz2eszps%o!5!+*#1@+*83gmp$o(u3%!ldp'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool_env(os.environ.get('DJANGO_DEBUG', False))

ALLOWED_HOSTS = ['*', ]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrapform',
    'apps.accounts',
    'apps.home',
    'apps.patient',
    'social_django',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
)
ROOT_URLCONF = 'bbc.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                'django_settings_export.settings_export',
            ],
        },
    },
]

WSGI_APPLICATION = 'bbc.wsgi.application'


MESSAGE_TAGS = {messages.DEBUG: 'debug',
                messages.INFO: 'info',
                messages.SUCCESS: 'success',
                messages.WARNING: 'warning',
                messages.ERROR: 'danger'
                }

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DBPATH = os.path.join(BASE_DIR, 'db/db.db')
DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.sqlite3',
        # Or path to database file if using sqlite3.
        'NAME': DBPATH,
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        # Set to empty string for localhost. Not used with sqlite3.
        'HOST': '',
        # Set to empty string for default. Not used with sqlite3.
        'PORT': '',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'collectstatic')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'sitestatic'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


AUTH_PROFILE_MODULE = 'accounts.UserProfile'
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'apps.accounts.oauth_backends.oauth2_io.OAuth2ioOAuth2')


# python-social-auth settings
SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_URL_ENTRY = 'social-auth'
SOCIAL_AUTH_OAUTH2IO_KEY = ''
SOCIAL_AUTH_OAUTH2IO_SECRET = ''
SOCIAL_AUTH_OAUTH2IO_SCOPE = []
# experimenting with setting name
SOCIAL_AUTH_OAUTH2IO_NAME = "oauth2io"
SOCIAL_AUTH_OAUTH2IO_STATE_PARAMETER = True

# Redirect_uri to be used in your target server is:
#

OAUTH2IO_HOST = "https://sandbox.bluebutton.cms.gov/v1"

FHIR_BASE_ENDPOINT = "%s/v1/fhir/" % (OAUTH2IO_HOST)
USER_INFO_ENDPOINT = "%s/v1/connect/userinfo/" % (OAUTH2IO_HOST)
FHIR_METADATA_URI = "%smetadata" % (FHIR_BASE_ENDPOINT)
OIDC_DISCOVERY_URI = "%s/.well-known/openid-configuration" % (OAUTH2IO_HOST)

OAUTH2_PROVIDER_NAME = "CMS"
APP_TITLE = "Blue Button Client Example"
SOCIAL_AUTH_ALWAYS_ASSOCIATE = True
# the trailing slash is necessary, because python-social-auth does not follow
# redirects by default.
# TRAILING_SLASH = False
# SOCIAL_AUTH_TRAILING_SLASH = TRAILING_SLASH
FHIR_HOST = OAUTH2IO_HOST + '/fhir'

LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL = '/accounts/login-error'
HOSTNAME_URL = "http://bbc:8001"

# Redirect_uri to be used in your target server is:
# HOSTNAME_URL + SOCIAL_AUTH_URL_ENTRY + '/complete/' + SOCIAL_AUTH_OAUTH2IO_NAME + '/'

# http://localhost:8001/social-auth/complete/oauth2io/

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.mail.mail_validation',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.debug.debug',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'social_core.pipeline.debug.debug'
)


SETTINGS_EXPORT = [
    'OAUTH2_PROVIDER_NAME',
    'OAUTH2IO_HOST',
    'FHIR_HOST',
    'APP_TITLE',
    'USER_INFO_ENDPOINT',
    'OIDC_DISCOVERY_URI',
    'FHIR_METADATA_URI',
]
