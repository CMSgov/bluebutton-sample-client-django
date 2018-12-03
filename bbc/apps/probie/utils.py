#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

"""
Project: bbc_pd
App: apps.probie
FILE: utils.py
Created: 6/13/18 11:59 PM

Created by: '@ekivemark'
"""

import json

from django.conf import settings
from requests_oauthlib import OAuth2

from .settings import (JSON_INDENT, STR_PRE, STR_POST)


def get_oauth_token(request):
    # first we get the token used to login
    token = request.user.social_auth.get(provider='oauth2io').access_token
    auth = OAuth2(
        settings.SOCIAL_AUTH_OAUTH2IO_KEY,
        token={
            'access_token': token,
            'token_type': 'Bearer'
        })
    return auth


def next_pathname(parent_name, item):
    """

    :param parent_name:
    :param item:
    :return:
    """
    if len(parent_name) > 0:
        pathname = "%s.%s" % (parent_name, str(item))
    else:
        pathname = "%s" % (str(item))

    return pathname


def next_pathseq(parent_seq, seq):
    """

    :return:
    """
    if parent_seq in ['0', '0.', '.']:
        pathseq = "%s" % (str(seq))
    else:
        pathseq = "%s.%s" % (parent_seq, str(seq))

    return pathseq


def probie_dict(item, val, seq=0, ilist=[], parent_name="", parent_seq="0"):
    """
    Receive item and value and return probie_dict
    :param item:
    :param val:
    :return:
    """

    o_dict = {}
    o_dict['name'] = item
    o_dict['type'] = type(val).__name__
    o_dict['value'] = val

    # print("Parent/Item:%s / %s" % (parent_name, str(item)))

    o_dict['pathName'] = next_pathname(parent_name, str(item))

    # print("pathName:%s" % o_dict['pathName'])

    o_dict['pathSeq'] = next_pathseq(parent_seq, seq)

    o_dict['level'] = o_dict['pathSeq'].count(".")
    o_dict['subset'] = ilist

    return o_dict


def get_fhir_dict(idict={}, parent_name="", parent_seq="0", flatten=False):
    """
    Pass in a dict and evaluate
    :param idict:
    :return: dict with fields {name, type, value, pathName, pathSeq}
    """

    o_list = []
    seq = 0

    for item, val in idict.items():
        oo_list = []

        if type(val) is dict:
            oo_list = get_fhir_dict(val,
                                    next_pathname(parent_name, str(item)),
                                    next_pathseq(parent_seq, seq),
                                    flatten)
        elif type(val) is list:
            # print("Item[type]:%s[%s]" % (item, type(item)))
            # print("List Parent:%s" % parent_name)
            oo_list = get_fhir_list(val,
                                    next_pathname(parent_name, str(item)),
                                    next_pathseq(parent_seq, seq),
                                    flatten)

        elif type(val) is int:
            oo_list = []
        else:
            oo_list = []

        o = probie_dict(item, val, seq, oo_list, parent_name, parent_seq)

        # o = {}
        # o['name'] = item
        # o['type'] = type(val).__name__
        # o['value'] = val
        # o['pathName'] = parent_name + item
        # o['pathSeq'] = "%s.%s" % (parent_seq, str(seq))

        o_list.append(o)
        if flatten:
            if len(oo_list) > 0:
                for i in oo_list:
                    o_list.append(i)

        seq += 1

    if o_list:
        if len(o_list) > 0:
            return o_list
    else:
        return


def get_fhir_list(ilist=[], parent_name="", parent_seq="0", flatten=False):
    """
    Pass in list and evaluate
    :param ilist:
    :param parent_name:
    :param parent_seq:
    :return: dict with fields {name, type, value, pathName, pathSeq}
    """

    o_list = []
    o_dict = []
    seq = 0

    for item in ilist:
        oo_list = []
        if type(item) in [dict, list]:
            if type(item) is dict:
                # print("Parent_name/item:%s / %s" % (parent_name, item))
                oo_list = get_fhir_dict(item,
                                        next_pathname(parent_name,
                                                      str(seq)),
                                        next_pathseq(parent_seq, seq),
                                        flatten)
            else:
                oo_list = get_fhir_list(item,
                                        next_pathname(parent_name,
                                                      str(seq)),
                                        next_pathseq(parent_seq, seq),
                                        flatten)

            o_dict = probie_dict(str(seq),
                                 item,
                                 seq,
                                 oo_list,
                                 next_pathname(parent_name, str(seq)),
                                 next_pathseq(parent_seq, seq))
        else:
            # string
            # integer
            o_dict = probie_dict(str(seq), item, seq, [], parent_name,
                                 parent_seq)
        o_list.append(o_dict)
        if flatten:
            if len(oo_list) > 0:
                for i in oo_list:
                    o_list.append(i)

        seq += 1

    return o_list


class Formatter(object):
    """
    Based on https://stackoverflow.com/questions/3229419/how-to-pretty-print-nested-dictionaries
    """
    def __init__(self):
        self.types = {}
        self.htchar = '\t'
        self.lfchar = '\n'
        self.indent = 0
        self.set_formater(object, self.__class__.format_object)
        self.set_formater(dict, self.__class__.format_dict)
        self.set_formater(list, self.__class__.format_list)
        self.set_formater(tuple, self.__class__.format_tuple)

    def set_formater(self, obj, callback):
        self.types[obj] = callback

    def __call__(self, value, **args):
        for key in args:
            setattr(self, key, args[key])
        formater = self.types[type(value) if type(value) in self.types else object]
        return formater(self, value, self.indent)

    def format_object(self, value, indent):
        return "'%s%s%s'" % (STR_PRE,
                             value,
                             STR_POST)

    def format_dict(self, value, indent):
        items = [
            self.lfchar + self.htchar * (indent + 1) + repr(key) + ': ' + (self.types[type(value[key])
                                                                           if type(value[key]) in self.types else object])(self, value[key], indent + 1)
            for key in value
        ]
        return '{%s}' % (','.join(items) + self.lfchar + self.htchar * indent)

    def format_list(self, value, indent):
        items = [
            self.lfchar + self.htchar * (indent + 1) + (self.types[type(item)
                                                        if type(item) in self.types else object])(self, item, indent + 1)
            for item in value
        ]
        return '[%s]' % (','.join(items) + self.lfchar + self.htchar * indent)

    def format_tuple(self, value, indent):
        items = [
            self.lfchar + self.htchar * (indent + 1) + (self.types[type(item)
                                                        if type(item) in self.types else object])(self, item, indent + 1)
            for item in value
        ]
        return '(%s)' % (','.join(items) + self.lfchar + self.htchar * indent)


def is_number(var):
    """
    Test value for integer
    :param var:
    :return: True | False
    """
    try:
        int(var)
        return True
    except TypeError:
        return False


class FindKey(dict):
    """
    Return content of a dict based on key
    Handles Dict and Lists
    Based on https://stackoverflow.com/questions/25833613/python-safe-method-to-get-value-of-nested-dictionary
    """
    def get(self, path, default=None):
        keys = path.split(".")
        val = None
        for key in keys:
            if val:
                if isinstance(val, list):
                    if int(key) <= len(val):
                        val = val[int(key)]
                    else:
                        val = default
                else:
                    val = val.get(key, default)
            else:
                val = dict.get(self, key, default)
            if not val:
                break
        return val


def show_html_name(name=""):
    """
    Pass in text value
    :param name:
    :return html_string
    """

    if name:
        return "<b>%s:</b>" % name


def show_txtval(display={}):
    """
    pass in a dict and return html display string
    :param display:
    :return:
    """

    html_out = ""

    if display is None:
        return None

    else:
        if 'name' in display:
            html_out += show_html_name(display['name'])
        if 'value' in display:
            html_out += "%s" % display['value']

    if html_out != "":
        return html_out
    else:
        return


def show_array(display={}):
    """
    pass in a dict or list and return display string
    :param display:
    :return:
    """

    html_out = ""

    if display is None:
        return None

    # print("Display:%s" % display)

    if type(display).__name__ == "list":
        for name in display:
            html_out += show_html_name(name)
    elif type(display).__name__ == "dict":
        # print("anything dict")
        # print("display is:%s" % display)

        for i, v in display.items():
            # print("item is:%s = %s" % (i, v))
            html_out += "%s[%s]:%s" % (i,
                                       type(v).__name__,
                                       v)

    # elif 'type' in display:
    #     if display['type'] in ['dict']:
    #         html_out += show_html_name(display['name'])
    #         html_out += show_array(display['value'])
    #     else:
    #         html_out += show_html_name(display['name'])
    #         html_out += show_txtval(display['value'])

    if html_out == "":
        return
    else:
        return html_out


def process_response(response):
    """
    Get result from response and process the json or return error
    :param response:
    :return probie, content:
    """

    probie = {}
    if response.status_code in (200, 404):
        if response.json():

            probie['hierarchy'] = get_fhir_dict(response.json(),
                                                parent_name="",
                                                parent_seq="0",
                                                flatten=False)
            probie['flat'] = get_fhir_dict(response.json(),
                                           parent_name="",
                                           parent_seq="0",
                                           flatten=True)

            content = {'text': response.text,
                       'json': response.json(),
                       'error': 'problem reading content.',
                       'status_code': response.status_code}
        else:
            content = {'text': response.text,
                       'json': '',
                       'error': 'problem reading content.',
                       'status_code': response.status_code}
    elif response.status_code == 403:
        content = {'text': response.text,
                   'json': '',
                   'error': 'No read capability',
                   'status_code': response.status_code}
    elif response.status_code == 401:
        # print("We got a 401")
        content = {'text': response.text,
                   'status_code': response.status_code}
        if response.json():
            # print("We got json")
            content['json'] = response.json()
            if 'detail' in response.json():
                content['error'] = '%s: %s' % (response.status_code,
                                               response.json()['detail'])
            else:
                content['error'] = '%s Error from ' \
                                   'the server' % response.status_code
        else:
            content['json'] = {}
            content['error'] = '%s ' \
                               'Error from the server' % response.status_code
        # print("Content%s" % content)
    elif response.status_code <= 500:
        content = {'text': response.text,
                   'status_code': response.status_code}
        if response.json():
            content['json'] = response.json()
            if 'detail' in response.json():
                content['error'] = '%s: %s' % (response.status_code,
                                               response.json()['detail'])
            else:
                content['error'] = '%s ' \
                                   'Error from the server' % response.status_code
        else:
            content['json'] = {}
            content['error'] = '%s ' \
                               'Error from the server' % response.status_code
    else:
        content = {'text': response.text,
                   'json': '',
                   'error': '',
                   'status_code': response.status_code}

    # print(response.status_code)
    # print(response.json())
    # print(response.text)
    # print("==================")
    # print("Content%s" % content)

    # print("===== leaving process response=======")
    return probie, content


def is_bundle(json_dict={}):
    """
    Check if resourceType = Bundle
    :param json_dict:
    :return: True \ False
    """

    if 'resourceType' in json_dict:
        if json_dict['resourceType'].lower() == 'bundle':
            return True

    if type(json_dict) == 'list':
        # print("Type:%s\nLength:%s" % (type(json_dict), len(json_dict)))

        if 'value' in json_dict[0]:
            if json_dict[0]['value'].lower() == 'bundle':
                return True

    return False


def get_entries(json_dict):
    """
    Get dict and look for entries

    :param json_dict:

    :return entry:
    """

    entry = []
    seq = 0
    for i in json_dict:
        if i['name'].lower() == "entry":
            # entry = i['value']
            # entry = i
            entry = get_fhir_list(i['value'],
                                  parent_name="entry",
                                  parent_seq="",
                                  flatten=False)
            # display output
            # x = display_entry(entry)

        seq += 1
    return entry


def get_content_text(content):
    """
    Get content from request and convert to text for context
    :param content:
    :return content_text:
    """
    if 'json' in content:
        if content['json']:
            content_text = json.dumps(content['json'], indent=JSON_INDENT)
        else:
            content_text = json.dumps(content, indent=JSON_INDENT)

    else:
        content_text = ""

    return content_text


def display_entry(entry):
    """

    :param entry:
    :return:
    """
    for i in entry:
        # print("====entry:start====")
        # print("Name:%s [%s]Level:%s\n%s | %s " % (i['name'],
        #                                           i['type'],
        #                                           i['level'],
        #                                           i['pathName'],
        #                                           i['pathSeq']))
        # print("====entry:end====")
        pass
    return


def json_probe(deep_ref="", content_json={}):
    """
    Delve into a json document based on a pathName
    e.g. entry.0.resource.resourceType
    :param deep_ref:
    :param content_json:
    :return extracted_json:
    """
    # no json to deal with
    if not content_json:
        return

    # nothing to select, return everything
    if not deep_ref:
        return content_json

    # Now let's get selective

    elements = deep_ref.split('.')

    # print("Elements:%s" % elements)

    extracted_json = {}
    extracted_json = content_json
    parent_key = ""
    for e in elements:
        # print("Checking: %s[%s]" % (e, type(e)))
        extracted_json = json_probe_element(e, extracted_json, parent_key)
        parent_key = e

    # print("%s = %s" % (deep_ref, extracted_json))

    return extracted_json


def json_probe_element(e, element_json={}, parent_key=""):

    element = {}
    if is_number(e):
        e_type = int(e)
        # dealing with a list

        if parent_key in element:
            element[parent_key] = element_json[parent_key][e_type]

    else:
        e_type = e
        # print("%s[%s]" % (e_type, type(e_type)))

        if e_type in element_json:
            if parent_key:
                element[e_type] = element_json[parent_key][e_type]
            else:
                element[e_type] = element_json[e_type]
            # for k, v in element_json.items():
            #     if e_type == k:
            #         print("%s:%s" % (k, v))
            #
            #         element[k] = v

    # print("Leaving json_print_element")
    # print(element)
    return element
