from __future__ import absolute_import
from __future__ import unicode_literals

from django.conf.urls import patterns, include, url

from .views import *


urlpatterns = patterns('',
    url(r'^call-read$', call_read, name="call_read"),
    url(r'^call-write$', call_write, name="call_write"),
)
