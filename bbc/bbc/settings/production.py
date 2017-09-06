from .base import *

SECRET_KEY = "HHSCLIENT-e81)))_cdlv24!g$4)b&wq9fjn)p!vrs729idssk2qp7iy!u#"

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

# STATIC_URL = '//static-oauth.npi.io/static-c/'


SOCIAL_AUTH_MYOAUTH_KEY = ''
SOCIAL_AUTH_MYOAUTH_SECRET = ''
# the trailing slash is necessary, because python-social-auth does not follow
# redirects by default.
HHS_OAUTH_URL = "https://oauth2.npi.io"
MY_AUTHORIZATION_URL = ('%s/o/authorize/') % (HHS_OAUTH_URL)
MY_ACCESS_TOKEN_URL = '%s/o/token/' % (HHS_OAUTH_URL)
MY_USER_PROFILE_URL = '%s/connect/userinfo' % (HHS_OAUTH_URL)
