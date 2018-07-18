#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

"""
Project: bbc_pd
App: apps.probie
FILE: urls.py
Created: 6/10/18 5:45 PM

Created by: '@ekivemark'
"""

from __future__ import absolute_import
from __future__ import unicode_literals
from django.conf.urls import url

from .views import (get_json_metadata,
                    get_by_url,
                    get_url_with_auth,
                    show_custom_view,
                    get_custom_view)

urlpatterns = [
    url(r'^getmetadata$',
        get_json_metadata,
        name="probie_getmetadata"),
    url(r'^getbyurl$',
        get_by_url,
        name="probie_getbyurl"),
    url(r'^geturlwithauth$',
        get_url_with_auth,
        name="probie_geturlwithauth"),
    url(r'^getcustomview$',
        get_custom_view,
        name="probie_getcustomview"),
    url(r'^customview$',
        show_custom_view,
        name="probie_showcustomview"),

]
