from .base import *
import os



DEBUG = True
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

SECRET_KEY = "HHSCLIENT-LOCAL-_cdlv24!g$4)b&wq9fjn)p!vrs729idssk2qp7iy!u#"

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

SOCIAL_AUTH_MYOAUTH_KEY = 'qexcETkxtyuXD3rSS8whIKz8MX8itgr5kO1djRMf'
SOCIAL_AUTH_MYOAUTH_SECRET = 'GdkWb0hTYbQDzljNhnnNxz5jmw563BNNrohbG7A59o9D1PCHj9RWc39RppFnFOcCtu05Obt38rwQaKqTHI3KGjvEpb2GDPniDeTbhf5WZEkJgXeWiAFalKVcXzZgGZYP'
SOCIAL_AUTH_MYOAUTH_EXTRA_ARGUMENTS = {'scope': 'blue-button-read-only provider-data-push'}
HHS_OAUTH_URL = "http://oauth:8000"
# HHS_OAUTH_URL = "https://cms.oauth2.io"
MY_AUTHORIZATION_URL = ('%s/o/authorize/') % (HHS_OAUTH_URL)
MY_ACCESS_TOKEN_URL =  '%s/o/token/' % (HHS_OAUTH_URL)
MY_USER_PROFILE_URL =  '%s/connect/userinfo' % (HHS_OAUTH_URL)
