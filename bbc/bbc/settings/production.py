from .base import *

SECRET_KEY = "HHSCLIENT-e81)))_cdlv24!g$4)b&wq9fjn)p!vrs729idssk2qp7iy!u#"

DBPATH=os.path.join(BASE_DIR, 'db/db.db')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': DBPATH,                   # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# STATIC_URL = '//static-oauth.npi.io/static-c/'


SOCIAL_AUTH_MYOAUTH_KEY = '0viv62YJiiV3YFsq0pOZ6Q5yMJpjhmzKXbmGKcOc'
SOCIAL_AUTH_MYOAUTH_SECRET = 'fyiFRWOfePo0YgQjKxQIufjsG5kuOvJorbBcgiPN2suIotaRcGQfBuIlX44zu3610Y0V9xy8Ii9504gt48JuhpQY0TPqmAsfSk6SVGdkL8u5sdogaTlbKVljV2GATzDB'
# the trailing slash is necessary, because python-social-auth does not follow
# redirects by default.
HHS_OAUTH_URL = "https://oauth2.npi.io"
MY_AUTHORIZATION_URL = ('%s/o/authorize/') % (HHS_OAUTH_URL)
MY_ACCESS_TOKEN_URL =  '%s/o/token/' % (HHS_OAUTH_URL)
MY_USER_PROFILE_URL =  '%s/connect/userinfo' % (HHS_OAUTH_URL)
