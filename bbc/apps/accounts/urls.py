#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from .views import my_logout


urlpatterns = [
    url(r'^logout', my_logout,  name="logout"),
]
