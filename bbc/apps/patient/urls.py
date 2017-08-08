from __future__ import absolute_import
from __future__ import unicode_literals

from django.conf.urls import include, url

from .views import bbof_pull_me, djmongo_read, djmongo_write


urlpatterns = [
    url(r'^cms/pull/me$', bbof_pull_me,  name="bbof_pull_me"),
    url(r'^djmongo-read$', djmongo_read,  name="djmongo_read"),
    url(r'^djmongo-write$', djmongo_write,  name="djmongo_write"),

]
