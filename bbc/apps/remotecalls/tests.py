from __future__ import absolute_import
from __future__ import unicode_literals

import json
from unittest import skipIf

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase, override_settings

from social.apps.django_app.default.models import UserSocialAuth

from ..test import BaseApiTest


def no_test_server_credentials():
    """
    Helper function that returns true when TEST_INTEGRATION_*
    credentials are undefined or empty.
    """
    client_id = getattr(settings, 'TEST_INTEGRATION_CLIENT_ID', None)
    username = getattr(settings, 'TEST_INTEGRATION_USERNAME', None)
    password = getattr(settings, 'TEST_INTEGRATION_PASSWORD', None)
    app_read = getattr(settings, 'TEST_INTEGRATION_READ_CLIENT_ID', None)
    app_write = getattr(settings, 'TEST_INTEGRATION_WRITE_CLIENT_ID', None)
    return not (client_id and username and password and app_read and app_write)


@skipIf(no_test_server_credentials(), "TEST_INTEGRATION_* settings are empty or undefined")
class TestCallViews(BaseApiTest):
    def _create_user(self, client_id):
        user = super(TestCallViews, self)._create_user('test_user', '123456')
        # request a token using the application with read/write capabilities
        # associate the token to the social_auth profile (this is usually
        # done by psa but here we do this manually to test both read and write
        # applications.)
        token = self._get_test_access_token(client_id)
        UserSocialAuth.objects.create(user=user, provider='myoauth', uid=1,
                                      extra_data={'access_token': token})
        return user

    @override_settings(SOCIAL_AUTH_MYOAUTH_KEY=settings.TEST_INTEGRATION_CLIENT_ID)
    def test_read_call_not_allowed_with_no_read_capability(self):
        # create a user with an access_token bound to the application
        # that has no write capability
        self._create_user(settings.TEST_INTEGRATION_CLIENT_ID)
        self.client.login(username="test_user", password="123456")
        response = self.client.get(reverse('call_read'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['remote_status_code'], 403)

    @override_settings(SOCIAL_AUTH_MYOAUTH_KEY=settings.TEST_INTEGRATION_READ_CLIENT_ID)
    def test_read_call_allowed_when_user_has_read_capability(self):
        # create a user with an access_token bound to the application
        # that has read capabilities.
        self._create_user(settings.TEST_INTEGRATION_READ_CLIENT_ID)
        self.client.login(username="test_user", password="123456")
        response = self.client.get(reverse('call_read'))
        self.assertEqual(response.context['remote_status_code'], 200)
        remote_content = json.dumps(response.context['remote_content'])
        self.assertJSONEqual(remote_content, {'hello': 'World', 'oauth2': True})

    @override_settings(SOCIAL_AUTH_MYOAUTH_KEY=settings.TEST_INTEGRATION_CLIENT_ID)
    def test_write_call_not_allowed_with_no_write_capability(self):
        # create a user with an access_token bound to the application
        # that has no write capability
        self._create_user(settings.TEST_INTEGRATION_CLIENT_ID)
        self.client.login(username="test_user", password="123456")
        response = self.client.post(reverse('call_write'), {'json': '{"foo": "bar"}'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['remote_status_code'], 403)

    @override_settings(SOCIAL_AUTH_MYOAUTH_KEY=settings.TEST_INTEGRATION_WRITE_CLIENT_ID)
    def test_write_call_allowed_when_user_has_write_capability(self):
        # create a user with an access_token bound to the application
        # that has write capabilities.
        self._create_user(settings.TEST_INTEGRATION_WRITE_CLIENT_ID)
        self.client.login(username="test_user", password="123456")
        response = self.client.post(reverse('call_write'), {'json': '{"foo": "bar"}'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['remote_status_code'], 200)
        remote_content = json.dumps(response.context['remote_content'])
        self.assertJSONEqual(remote_content, {'foo': 'bar', 'write': True})
