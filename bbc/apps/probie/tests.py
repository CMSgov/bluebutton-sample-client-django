#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

"""
Project: bbc_pd
App: apps.probie
FILE: tests
Created: 6/10/18 10:51 PM

Created by: ''
"""

import os
import json
# import pprint
from django.test import TestCase
from django.test.client import Client

from django.conf import settings

from .views import (get_fhir_dict,
                    show_html_name,
                    show_txtval,
                    show_array)


class testContent(TestCase):
    """
    Test fhir content
    """

    def test_get_fhir_dict(self):
        """
        What is returned from capabilityStatement.json
        :return:
        """

        target_file =  os.path.join(settings.BASE_DIR,
                                    'apps/fhirengine/capabilityStatement.json')
        with open(target_file) as f:
            data = json.load(f)

        result = get_fhir_dict(data)

        expected = "CapabilityStatement"

        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(result)

        self.assertTrue(result[0]['name'], expected)

    def test_no_fhir_content(self):
        """
        Nothing received. nothing returned.
        :return:
        """
        result = get_fhir_dict()

        self.assertIsNone(result)


class testShowTextValue(TestCase):
    """
    Test fhir element display
    """

    def test_show_no_text(self):
        """
        Nothing received. Nothing returned
        :return:
        """

        result = show_txtval()

        self.assertIsNone(result)

    def test_show_bad_dict_text(self):
        """
        Get a bad dict - show nothing.
        :return:
        """

        bad_dict = {"anythingbad": "rubbish",
                    "morecrap": "yes_it_is_crap"}

        result = show_txtval(bad_dict)

        self.assertIsNone(result)

    def test_show_partial_dict_text(self):
        """
        Get a name but no value
        :return:
        """

        soso_dict = {"name": "name is okay",
                     "morecrap": "yes_it_is_crap"}

        result = show_txtval(soso_dict)

        expected = "<b>%s:</b>" % soso_dict['name']
        self.assertTrue(result, expected)

    def test_show_full_dict_text(self):
        """
        get a proper dict. Return a full string
        :return:
        """
        good_dict = {"name": "name is okay",
                     "type": "string",
                     "value": "yes_it_is_good"}

        result = show_txtval(good_dict)

        expected = "<b>%s:</b>%s" % (good_dict['name'], good_dict['value'])
        self.assertTrue(result, expected)

    def test_show_full_dict_value(self):
        """
        get proper dict. Return Value.
        :return:
        """
        good_dict = {"name": "value is okay",
                     "type": "int",
                     "value": 100.10}

        result = show_txtval(good_dict)

        expected = "<b>%s:</b>%s" % (good_dict['name'], good_dict['value'])
        self.assertTrue(result, expected)


class testShowName(TestCase):
    """
    pass in text
    """

    def test_show_no_name(self):
        """"
        pass in nothing. Return nothing.
        :return:
        """

        result = show_html_name()

        self.assertIsNone(result)

    def test_show_name(self):
        """
        pass in string. return name formatted.
        :return: string
        """

        name = "Pass in name to display"
        result = show_html_name(name)

        expected = "<b>%s:</b>" % name

        self.assertTrue(result, expected)


class testShowArray(TestCase):
    """
    Test FHIR array display
    """

    def test_show_no_array(self):
        """
        Pass in nothing. Return nothing.
        :return:
        """

        result = show_array()

        self.assertIsNone(result)

    def test_show_array_list_text(self):
        """
        pass in array.
        :return:
        """

        a_list = ['field_0', 'field_1', 'field_2', 'field_3']

        result = show_array(a_list)

        expected = show_html_name(a_list[0])
        expected += show_html_name(a_list[1])
        expected += show_html_name(a_list[2])
        expected += show_html_name(a_list[3])

        self.assertTrue(result, expected)

    def test_show_array_dict(self):
        """
        pass in dict
        :return:
        """

        a_dict = {"name": "field_a",
                  "type": "string",
                  "value": "this is field A"}

        result = show_array(a_dict)

        expected = None

        print(result)

        self.assertTrue(result, expected)
