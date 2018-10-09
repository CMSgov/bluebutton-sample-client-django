from .base import *  # noqa
# import os


DEBUG = True

# change this key for your environment
SECRET_KEY = "change-meiva8i*!ox)d(919hiy8zecc3&q)*=bophl@kzw05gick(&$wb7"

# Uncomment the next line and "import os" to operate over http. DO NOT in production.
# os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Set these values for you environment
SOCIAL_AUTH_OAUTH2IO_KEY = ''
SOCIAL_AUTH_OAUTH2IO_SECRET = ''
SOCIAL_AUTH_OAUTH2IO_SCOPE = []
OAUTH2_PROVIDER_NAME = "Your OAuth2"
APP_TITLE = "Sample Application Title"

# Uncomment the following line to point to another authorization service.
# OAUTH2IO_HOST = "http://localhost:8000"
