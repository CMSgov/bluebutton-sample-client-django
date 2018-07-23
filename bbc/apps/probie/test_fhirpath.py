#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

"""
Project: bbc_pd
App: apps.probie
FILE: test_fhirpath.py
Created: 6/10/18 10:51 PM

Created by: '@ekivemark'
"""

import os
import json
# import pprint
from django.test import TestCase
from django.test.client import Client

from django.conf import settings

from .utils import (get_fhir_dict,
                    show_html_name,
                    show_txtval,
                    show_array)


class testFhirPath(TestCase):
    """
    Test fhir content
    """

    def test_get_fhir_dict(self):

        return
