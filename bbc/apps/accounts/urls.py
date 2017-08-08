#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from .views import *


urlpatterns = [

    url(r'login', my_login,  name="login"),
    url(r'logout', my_logout,  name="logout"),
]
