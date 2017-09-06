"""
WSGI config for bbc project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""
import os
import sys
from django.core.wsgi import get_wsgi_application

__author__ = "Alan Viars"

sys.path.append('/home/ubuntu/django-projects/django_bluebutton_client/bbc')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bbc.settings.production")
application = get_wsgi_application()
