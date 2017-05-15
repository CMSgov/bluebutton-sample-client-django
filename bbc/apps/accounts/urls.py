#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from .views import *


urlpatterns = patterns('',

    url(r'login', my_login,  name="login"),
    url(r'logout', my_logout,  name="logout"),
)
