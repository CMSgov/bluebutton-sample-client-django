from .base import *

HHS_OAUTH_URL = "http://oauth.npi.io"
MY_AUTHORIZATION_URL = 'http://oauth.npi.io/o/authorize/'
MY_ACCESS_TOKEN_URL =  'http://oauth.npi.io/o/token/'
MY_USER_PROFILE_URL =  'http://oauth.npi.io/api/profile/'

SOCIAL_AUTH_MYOAUTH_KEY = 'f9BL8Q16PRBrsbZocmmDkV5Q03wma0eWouOWx25z'
SOCIAL_AUTH_MYOAUTH_SECRET = 'tymFpjhaoy8QKrKwm4JSzRtZ1k5RtEQkl9AHSLDM722qeG4ClxjGq076NuAxpEoR4HREeATKr8FCxyz17a2U0R1y0x0u9BuEgPGFMBTCHbBBxAV9dfmSBl6PJInetw7B'

# this is the client id of the application used to obtain tokens
# with the password flow in the integration tests.
# the app is defined in the staging server: http://oauth.npi.io
TEST_INTEGRATION_CLIENT_ID = 'test_app'
TEST_INTEGRATION_USERNAME = 'test_user'
TEST_INTEGRATION_PASSWORD = 'foobarbaz'

TEST_INTEGRATION_READ_CLIENT_ID = 'test_app_read'
TEST_INTEGRATION_WRITE_CLIENT_ID = 'test_app_write'

# this env variable is needed by oauthlib to disable the SSL
# check while testing, because the testing server doesn't use SSL
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
