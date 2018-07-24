#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

"""
Project: bbc_pd
App: apps.probie

FYI: A Probie is a Probationary Firefighter.
FILE: views.py
Created: 6/10/18 5:45 PM

Created by: '@ekivemark'
"""

from __future__ import absolute_import
from __future__ import unicode_literals
import json

import logging

try:
    from urllib.parse import (urljoin,
                              urlparse,
                              urlsplit,
                              parse_qsl,
                              urlencode)
except ImportError:
    from urllib import urlencode
    from urlparse import urljoin, urlparse, urlsplit, parse_qsl

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import requests
from requests_oauthlib import OAuth2
from .settings import (PROBIE_NAME, PROBIE_DEF, JSON_INDENT)
from .utils import (get_fhir_dict,
                    get_oauth_token,
                    process_response,
                    is_bundle,
                    get_entries,
                    get_content_text,
                    json_probe)
from .forms import getUrlForm, getCustomViewForm
from ..patient.views import build_fhir_urls
from .settings_custom_view import CUSTOM_VIEW

__author__ = "@ekivemark"


@login_required
def get_json_metadata(request):
    """
    Get the CapabilityStatement / metadata
    :param request:
    :return:
    """
    patient_id = None
    urls = build_fhir_urls(patient_id)
    # print(urls)
    # resource_type = "patient"
    resource_type = "metadata"

    # print("Made it to endpoint")

    # first we get the OAuth token used to login
    auth = get_oauth_token(request)

    # next we call the remote api
    if resource_type.lower() == "metadata":
        endpoint = '/v1/fhir/%s?_format=json' % resource_type
    else:
        endpoint = urls['%s%s' % (resource_type, '_search')]

    url = urljoin(
        getattr(settings, 'OAUTH2IO_HOST',
                "https://sandbox.bluebutton.cms.gov"), endpoint)
    # % (request.user.username)

    logging.debug("calling FHIR Service with %s" % url)

    response = requests.get(url, auth=auth)

    probie, content = process_response(response)
    if 'hierarchy' in probie:
        fe_d = probie['hierarchy']
    else:
        fe_d = {}

    context = {'name': PROBIE_NAME}
    context['target_url'] = url
    context['fe_dict'] = fe_d
    context['remote_status_code'] = response.status_code
    context['remote_content'] = get_content_text(content)
    context['What_is_a_Probie'] = PROBIE_DEF
    return render(request, 'engine_f.html', context)


@login_required
def get_by_url(request):
    # if this is a POST request we need to process the form data
    # print("in get_by_url")
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = getUrlForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            # print("URL:%s" % form.cleaned_data['url'])
            # return view_any_url(request, form.cleaned_data['url'])
            return view_any_url_bundle(request, form.cleaned_data['url'])

    # if a GET (or any other method) we'll create a blank form
    else:
        # print("Doing get in get_by_url")
        form = getUrlForm(initial={'url': 'https://sandbox.bluebutton.'
                                          'cms.gov/v1/fhir/metadata'})

    return render(request, 'ask_for_url.html', {'form': form})


@login_required
def get_custom_view(request):
    # if this is a POST request we need to process the form data
    # print("in get_by_url")
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = getCustomViewForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            # print("URL:%s" % form.cleaned_data['url'])
            return custom_view_url(request,
                                   form.cleaned_data['url'],
                                   form.cleaned_data['custom_view'])

    # if a GET (or any other method) we'll create a blank form
    else:
        # print("Doing get in get_by_url")
        form = getCustomViewForm(initial={'url': 'https://sandbox.bluebutton.'
                                                 'cms.gov/v1/fhir/metadata'})

    return render(request, 'ask_for_custom_view.html', {'form': form})


@login_required
def view_any_url(request, url):
    """
    Get the url
    :param request:
    :param url:
    :return:
    """

    # print("Made it to view any url endpoint")

    # first we get the OAuth token used to login
    auth = get_oauth_token(request)

    logging.debug("calling FHIR Service with %s" % url)

    response = requests.get(url, auth=auth)

    probie, content = process_response(response)
    if 'hierarchy' in probie:
        fe_d = probie['hierarchy']
    else:
        fe_d = {}

    context = {'name': PROBIE_NAME}
    context['target_url'] = url
    context['fe_dict'] = fe_d
    context['remote_status_code'] = response.status_code
    context['remote_content'] = get_content_text(content)
    context['What_is_a_Probie'] = PROBIE_DEF
    return render(request, 'engine_f.html', context)


@login_required
def custom_view_url(request, url, view=None):
    """
    Get the url
    :param request:
    :param url:
    :param view:
    :return:
    """
    if view:
        custom_view_name = view
    else:
        custom_view_name = "Patient"

    # first we get the OAuth token used to login
    auth = get_oauth_token(request)

    logging.debug("calling Custom FHIR viewer for %s" % url)

    response = requests.get(url, auth=auth)

    probie, content = process_response(response)

    fe_d = probie['hierarchy']
    if 'hierarchy' in probie:
        fe_d = probie['hierarchy']
    else:
        fe_d = {}

    custom_view_list = [item for item in CUSTOM_VIEW
                        if item['view'] == custom_view_name]
    # print("Custom Selection: %s" % custom_view_list)
    # print("\n")

    fe_d_subset = []

    for fe_i in fe_d:
        # print(fe_i['pathName'])

        for c_v_l in custom_view_list:
            if fe_i['pathName'] == c_v_l['pathName']:
                # print("Matched:%s" % fe_i['pathName'])
                fe_d_subset.append(fe_i)
                if c_v_l['display_title']:
                    fe_i['name'] = c_v_l['display_title']
            else:
                # print("No match:%s with %s" % (fe_i['pathName'], c_v_p))
                pass

    context = {'name': PROBIE_NAME}
    context['fe_dict_source'] = fe_d
    context['view'] = custom_view_name
    context['target_url'] = url
    context['fe_dict'] = fe_d_subset
    if 'flat' in probie:
        context['fe_flat'] = probie['flat']
    else:
        context['fe_flat'] = {}
    context['remote_status_code'] = response.status_code
    context['remote_content'] = get_content_text(content)
    context['What_is_a_Probie'] = PROBIE_DEF
    return render(request, 'custom_view.html', context)


def get_url_with_auth(request):
    """
    Make a call to a url with the oauth token added to the header
    and pass to viewer
    :param request:
    :param url:
    :return:
    """

    url = request.GET.get('url')
    # print("we got here with %s" % url)

    # return view_any_url(request, url)
    return view_any_url_bundle(request, url)


def show_custom_view(request):
    """
    Make a call to a url with the oauth token added to the header
    and pass to a custom viewer
    :param request:
    :return:
    """

    view = request.GET.get('view')
    url = request.GET.get('url')

    return custom_view_url(request, url, view)


@login_required
def view_any_url_bundle(request, url):
    """
    Get the url
    :param request:
    :param url:
    :return:
    """
    # print("Made it to view bundle url endpoint")

    # first we get the OAuth token used to login
    auth = get_oauth_token(request)

    logging.debug("calling FHIR Service with %s" % url)

    response = requests.get(url, auth=auth)

    probie, content = process_response(response)
    if 'hierarchy' in probie:
        fe_d = probie['hierarchy']
    else:
        fe_d = {}

    entry = []
    template_file = "engine_f.html"
    bundle_info = {}

    if fe_d:
        if is_bundle(content['json']):
            bundle_info['resourceType'] = content['json']['resourceType']
            bundle_info['total'] = content['json']['total']
            bundle_info['link'] = content['json']['link']
            if int(bundle_info['total']) > 0:
                bundle_info['entryType'] = content['json']['entry'][0]['resource']['resourceType']
                bundle_info['entryCount'] = int(len(content['json']['entry']))
            else:
                bundle_info['entryType'] = ""
                bundle_info['entryCount'] = "0"
            entry = get_entries(fe_d)

            template_file = "bundle_f.html"

    context = {'name': PROBIE_NAME}
    context['target_url'] = url
    context['fe_dict'] = fe_d
    if 'flat' in probie:
        context['fe_flat'] = probie['flat']
    else:
        context['fe_flat'] = {}
    context['entry'] = entry
    context['bundle'] = bundle_info
    context['remote_status_code'] = response.status_code
    context['remote_content'] = get_content_text(content)
    context['What_is_a_Probie'] = PROBIE_DEF
    context['show_footnote'] = True
    return render(request, template_file, context)
