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
from .utils import get_fhir_dict, get_oauth_token
from .forms import getUrlForm
from ..patient.views import build_fhir_urls

__author__ = "@ekivemark"

CUSTOM_VIEW = [
    {'view': 'Patient',
     'display_title': '',
     'pathName': 'resourceType'},
    {'view': 'Patient',
     'display_title': 'Patient Identifier',
     'pathName': 'identifier.0.value'},
    {'view': 'Patient',
     'display_title': 'Patient Name',
     'pathName': 'name.0.given.0'},
    {'view': 'Patient',
     'display_title': 'Patient Last Name',
     'pathName': 'name.0.family'},
    {'view': 'Patient',
     'display_title': 'Date of Birth',
     'pathName': 'birthDate'},
    {'view': 'Patient',
     'display_title': 'Patient Zip Code',
     'pathName': 'address.0.postalCode'},
    {'view': "Patient",
     "display_title": "State",
     "pathName": "address.0.state"},
    {'view': 'Coverage',
     'display_title': '',
     'pathName': ''},

]


@login_required
def get_json_metadata(request):
    """
    Get the CapabilityStatement / metadata
    :param request:
    :return:
    """
    context = {'name': 'HL7 FHIR Probie'}
    patient_id = None
    urls = build_fhir_urls(patient_id)
    # print(urls)
    # resource_type = "patient"
    resource_type = "metadata"

    # print("Made it to endpoint")

    # first we get the OAuth token used to login
    auth =  get_oauth_token(request)

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

    fe_d = {}
    if response.status_code in (200, 404):
        if response.json():
            fe = response.json()
            fe_d = get_fhir_dict(fe)

            content = json.dumps(response.json(), indent=4)
        else:
            content = {'error': 'problem reading content.'}
    elif response.status_code == 403:
        content = {'error': 'No read capability'}
        # content = response.content
    elif response.status_code <= 500:
        content = {
            'error': '500 Error from the server.',
            'status_code': response.status_code
        }
        # content = response.content
    else:
        content = response.content

    context['target_url'] = url
    context['fe_dict'] = fe_d
    context['remote_status_code'] = response.status_code
    context['remote_content'] = content
    context['What_is_a_Probie'] = "What is a Probie?<p>A <b>\'Probie\'</b> " \
                                  "is a " \
                                  "Probationary FireFighter</p>"
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
            return view_any_url(request, form.cleaned_data['url'])

    # if a GET (or any other method) we'll create a blank form
    else:
        # print("Doing get in get_by_url")
        form = getUrlForm(initial={'url': 'https://sandbox.bluebutton.'
                                          'cms.gov/v1/fhir/metadata'})

    return render(request, 'ask_for_url.html', {'form': form})


@login_required
def view_any_url(request, url):
    """
    Get the url
    :param request:
    :param url:
    :return:
    """
    context = {'name': 'HL7 FHIR Probie'}

    print("Made it to view any url endpoint")

    # first we get the OAuth token used to login
    auth = get_oauth_token(request)

    logging.debug("calling FHIR Service with %s" % url)

    response = requests.get(url, auth=auth)

    fe_d = {}
    if response.status_code in (200, 404):
        if response.json():
            fe = response.json()
            fe_d = get_fhir_dict(fe)

            content = json.dumps(response.json(), indent=4)
        else:
            content = {'error': 'problem reading content.'}
    elif response.status_code == 403:
        content = {'error': 'No read capability'}
        # content = response.content
    elif response.status_code <= 500:
        content = {
            'error': '500 Error from the server.',
            'status_code': response.status_code
        }
        # content = response.content
    else:
        content = response.content

    context['target_url'] = url
    context['fe_dict'] = fe_d
    context['remote_status_code'] = response.status_code
    context['remote_content'] = content
    context['What_is_a_Probie'] = "What is a Probie?<p>A <b>\'Probie\'</b> " \
                                  "is a " \
                                  "Probationary FireFighter</p>"
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
    context = {'name': 'HL7 FHIR Probie'}

    print("Made it to the custom viewer:%s" % view)

    if view:
        custom_view_name = view
    else:
        custom_view_name = "Patient"

    # first we get the OAuth token used to login
    auth = get_oauth_token(request)

    logging.debug("calling Custom FHIR viewer for %s" % url)

    response = requests.get(url, auth=auth)

    fe_d = {}
    if response.status_code in (200, 404):
        if response.json():
            fe = response.json()
            fe_d = get_fhir_dict(fe,
                                 parent_name="",
                                 parent_seq="0",
                                 flatten=True)

            content = json.dumps(response.json(), indent=4)
        else:
            content = {'error': 'problem reading content.'}
    elif response.status_code == 403:
        content = {'error': 'No read capability'}
        # content = response.content
    elif response.status_code <= 500:
        content = {
            'error': '500 Error from the server.',
            'status_code': response.status_code
        }
        # content = response.content
    else:
        content = response.content

    custom_view_list = [item for item in CUSTOM_VIEW if item['view'] == custom_view_name]
    # print("Custom Selection: %s" % custom_view_list)
    # print("\n")
    custom_view_paths = [itm['pathName'] for itm in custom_view_list]
    # print("Only Paths:%s" % custom_view_paths)
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


        # for c_v_p in custom_view_paths:
        #     if fe_i['pathName'] == c_v_p:
        #         # print("Matched:%s" % fe_i['pathName'])
        #         fe_d_subset.append(fe_i)
        #     else:
        #         # print("No match:%s with %s" % (fe_i['pathName'], c_v_p))
        #         pass

    # print("Subset:%s" % fe_d_subset)
    # print("\n")

    context['fe_dict_source'] = fe_d
    context['view'] = custom_view_name
    context['target_url'] = url
    context['fe_dict'] = fe_d_subset
    context['remote_status_code'] = response.status_code
    context['remote_content'] = content
    context['What_is_a_Probie'] = "What is a Probie?<p>A <b>\'Probie\'</b> " \
                                  "is a " \
                                  "Probationary FireFighter</p>"
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
    print("we got here with %s" % url)

    return view_any_url(request, url)


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
