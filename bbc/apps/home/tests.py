from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.conf import settings


class LoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('home')

    def test__login(self):
        """
        Valid User can login
        """
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, settings.APP_TITLE)
