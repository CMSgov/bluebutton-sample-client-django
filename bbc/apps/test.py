from __future__ import absolute_import
from __future__ import unicode_literals


from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from .accounts.oauth_backends.oauth2_io import OAuth2ioOAuth2


class BaseApiTest(TestCase):
    """
    This class contains some helper methods useful to test API endpoints
    protected with oauth2 using DOT.
    """

    def setUp(self):
        backend = OAuth2ioOAuth2()
        self.token_url = backend.ACCESS_TOKEN_URL

    def _create_user(self, username, password, **extra_fields):
        """
        Helper method that creates a user instance
        with `username` and `password` set.
        """
        user = User.objects.create_user(
            username, password=password, **extra_fields)
        return user

    def _get_test_access_token(self, client_id):
        """
        Helper method that returns an access token from the test server.
        """
        from oauthlib.oauth2 import LegacyApplicationClient
        from requests_oauthlib import OAuth2Session
        # get credentials for the test server
        username = getattr(settings, 'TEST_INTEGRATION_USERNAME', None)
        password = getattr(settings, 'TEST_INTEGRATION_PASSWORD', None)

        print("clientid", client_id)
        # get the access token with password flow
        oauth = OAuth2Session(
            client=LegacyApplicationClient(client_id=client_id))
        token = oauth.fetch_token(
            token_url=self.token_url,
            username=username, password=password, client_id=client_id)
        return token.get('access_token')
