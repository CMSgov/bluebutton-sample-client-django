# -*- coding: utf-8 -*-
from social.backends.oauth import BaseOAuth2

from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.conf import settings


class MyIDMMEOAuth2(BaseOAuth2):
    name                = 'idme'
    ID_KEY              = 'email'
    AUTHORIZATION_URL   = 'https://api.id.me/oauth/authorize/' #  'http://127.0.0.1:8000/o/authorize'
    ACCESS_TOKEN_URL    = 'https://api.id.me/oauth/token/'  #'http://127.0.0.1:8000/o/token'
    ACCESS_TOKEN_METHOD = 'POST'

    def get_user_profile_url(self):
        """
        Return the url to the user profile endpoint.
        """
        user_profile_url = 'https://api.id.me/api/public/v3/attributes.json'
        if not user_profile_url:
            raise ImproperlyConfigured("'MY_USER_PROFILE_URL' setting should be defined.")

        return user_profile_url

    def get_user_id(self, details, response):
        # Extracts the user id from `user_data` response.
        return response.get('email')

    def get_user_details(self, response):
        """
        Return user details from MYOAUTH account
        """
        
        print(response)
        return {
            'username': response.get('sub'),
            'first_name': response.get('given_name'),
            'last_name': response.get('family_name'),
            'email': response.get('email'),
        }

    def user_data(self, access_token, *args, **kwargs):
        """
        Loads user data from service
        """
        return self.get_json(self.get_user_profile_url(), params={'access_token': access_token})
