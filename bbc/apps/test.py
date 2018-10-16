from __future__ import absolute_import
from __future__ import unicode_literals

from django.test.client import Client
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from .accounts.oauth_backends.oauth2_io import OAuth2ioOAuth2
from django.core.serializers.json import DjangoJSONEncoder
from unittest import skipUnless, skip
from requests_oauthlib import OAuth2Session


# ENCODED = settings.ENCODING
#
#
# def can_reach_server():
#     backend = OAuth2ioOAuth2()
#     host = backend.OAUTH2IO_HOST
#     # client = Client()
#     # response = client.get(host)
#     # if response.status_code == 200:
#     #     print("Connected to:", host)
#     #     return True
#     # print("No connection to:", host)
#     # return False
#
#
# class BlueButtonApiTest(TestCase):
#     """
#     Test the BlueButton API Client
#     """
#
#     def setUp(self):
#         backend = OAuth2ioOAuth2()
#         self.oidc_discovery_url = backend.OAUTH2IO_HOST + "/.well-known/openid-configuration"
#         self.token_url = backend.ACCESS_TOKEN_URL
#         self.authorization_url =  backend.AUTHORIZATION_URL
#         self.redirect_uri = settings.HOSTNAME_URL  + "/social-auth/complete/oauth2io/"
#         self.client_id = settings.SOCIAL_AUTH_OAUTH2IO_KEY
#         self.client_secret = settings.SOCIAL_AUTH_OAUTH2IO_SECRET
#         print( self.authorization_url, )
#
#
#     # #@skipUnless(can_reach_server(), "Requires access to server.")
#     # def test_oidc_discovery(self):
#     #     """
#     #     Test Authorization_code_flow
#     #     """
#     #     c = Client()
#     #     response = c.get(self.oidc_discovery_url)
#     #     print("DICOVER", self.oidc_discovery_url )
#     #     self.assertEqual(response.status_code, 200)
#     #     jresponse = response.content.decode(ENCODED)
#     #     #print(jresponse)
#
#
#
#
#
#     def test_get_authorization_code_flow(self):
#         """
#         Test Authorization_code_flow
#         """
#         oas  = OAuth2Session(self.client_id, redirect_uri=self.redirect_uri)
#
#
#         print("redirect: ", self.redirect_uri)
#         print("client_id", settings.SOCIAL_AUTH_OAUTH2IO_KEY)
#
#         token = oas.fetch_token(self.token_url, client_secret=self.client_secret,
#                                 authorization_response=self.redirect_uri)
#         oas = OAuth2Session(client_id, token=token)
#         payload = oas.get(attributes_url).json()
#
#
#
#
#
#
#
#
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

    #@skipUnless(can_reach_server(), "Requires access to server.")
    # def _get_test_access_token(self, client_id):
    #     """
    #     Helper method that returns an access token from the test server.
    #     """
    #     print("hello")
    #
    #     from oauthlib.oauth2 import LegacyApplicationClient
    #     from requests_oauthlib import OAuth2Session
    #     # get credentials for the test server
    #     username = getattr(settings, 'TEST_INTEGRATION_USERNAME', None)
    #     password = getattr(settings, 'TEST_INTEGRATION_PASSWORD', None)
    #
    #     print("clientid", client_id)
    #     # get the access token with password flow
    #     oauth = OAuth2Session(
    #         client=LegacyApplicationClient(client_id=client_id))
    #     token = oauth.fetch_token(
    #         token_url=self.token_url,
    #         username=username, password=password, client_id=client_id)
    #     return token.get('access_token')



