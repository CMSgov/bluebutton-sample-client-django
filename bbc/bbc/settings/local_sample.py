from .base import *
import os


DEBUG = True

# This allows oauth to operate over http. DO NOT USE THIS CONFIG IN PRODUCTION
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

SECRET_KEY = "BBCLIENT-LOCAL-_cdlv24!g$4)b&wq9fjn)p!vrs729idssk2qp7iy!u#!"

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

# Set these values for you environment
SOCIAL_AUTH_OAUTH2IO_KEY = ''
SOCIAL_AUTH_OAUTH2IO_SECRET = ''
SOCIAL_AUTH_OAUTH2IO_SCOPE = []
OAUTH2IO_HOST = "http://example.com"
OAUTH2_PROVIDER_NAME = "Your OAuth2"
APP_TITLE = "Your Client Example"

