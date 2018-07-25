#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

"""
Project: bbc_pd
App: apps.probie
FILE: fhirbundle.py
Created: 7/24/18 14:01 PM

Created by: '@ekivemark'
"""

# import json
import logging

import requests
from .fhirpath import get_jpath
from .utils import get_oauth_token, process_response


# def build_oauth_token(access_token=""):
#     # first we get the token used to login
#     # token = request.user.social_auth.get(provider='oauth2io').access_token
#     token = access_token
#     auth = OAuth2(
#         settings.SOCIAL_AUTH_OAUTH2IO_KEY,
#         token={
#             'access_token': token,
#             'token_type': 'Bearer'
#         })
#     return auth
#
#
def get_full_bundle(auth, url):

    # first we get the OAuth token used to login
    # auth = get_oauth_token(access_token)

    logging.debug("calling FHIR Bundler with %s" % url)

    response = requests.get(url, auth=auth)

    probie, content = process_response(response)

    entry = get_jpath("$.entry.[*]", content['json'])

    start_index = 0
    if 'resourceType' in content['json']:
        if content['json']['resourceType'].lower() == 'bundle':
            if 'total' in content['json']:
                bundle_total = content['json']['total']
            else:
                bundle_total = 0
            if 'entry' in content['json']:
                this_bundle = len(content['json']['entry'])
                start_index += this_bundle
                # for e in content['json']['entry']:
                #     entry.append(e)
            else:
                this_bundle = 0

            while start_index < bundle_total:
                # we need to iterate over more bundles
                if 'next' in get_jpath('$.link.[*].relation', content['json']):
                    next_url = get_next_url(content['json']['link'])

                    response = requests.get(next_url, auth=auth)
                    probie, content = process_response(response)
                    more_entries, start_index = check_bundle_info(content['json'],
                                                                  start_index)
                    for m_e in more_entries:
                        # append entries to entry
                        entry.append(m_e)

                else:
                    start_index = bundle_total

    return entry


def get_next_url(json_link_list=[]):
    """
    get the url parameter for "next" from link list
    :param json_link:
    :return next_url:
    """

    next_url = ""
    for l in json_link_list:
        if 'relation' in l:
            if l['relation'].lower() == 'next':
                if 'url' in l:
                    next_url = l['url']
                    return next_url

    return next_url


def check_bundle_info(json_bundle={}, start_index=0):
    """
    Check the bundle information
    :param json_bundle:
    :return :
    """

    entry = []
    if 'resourceType' in json_bundle:
        if json_bundle['resourceType'].lower() == 'bundle':
            if 'total' in json_bundle:
                bundle_total = json_bundle['total']
            else:
                bundle_total = 0
            if 'entry' in json_bundle:
                this_bundle = len(json_bundle['entry'])
                start_index += this_bundle
                entry = get_jpath("$.entry.[*]", json_bundle)
            else:
                this_bundle = 0

    return entry, start_index