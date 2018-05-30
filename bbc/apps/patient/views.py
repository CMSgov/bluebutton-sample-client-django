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
from collections import OrderedDict
import requests
from requests_oauthlib import OAuth2

__author__ = "Alan Viars"


def build_fhir_urls(patient_id=None, since_date=None):
    result = {}
    base = getattr(settings, 'FHIR_BASE_ENDPOINT',
                   "https://sandbox.bluebutton.cms.gov/v1/fhir/")
    eob_search = urljoin(base, "ExplanationOfBenefit/")
    result['eob_search'] = eob_search
    patient_search = urljoin(base, "Patient/")
    result['patient_search'] = patient_search

    if patient_id:
        result['coverage'] = urljoin(base,
                                     "Coverage/?beneficiary=%s" % (patient_id))
        result['eob'] = urljoin(base, "ExplanationOfBenefit/?patient=%s" %
                                (patient_id))
        result['patient'] = urljoin(base, "Patient/%s" % (patient_id))
    return result


@login_required
def bbof_get_userinfo(request):
    context = {'name': 'Get Userinfo'}
    url = getattr(settings, 'USER_INFO_ENDPOINT',
                  "https://sandbox.bluebutton.cms.gov/v1/connect/userinfo")
    token = request.user.social_auth.get(provider='oauth2io').access_token
    auth = OAuth2(
        settings.SOCIAL_AUTH_OAUTH2IO_KEY,
        token={
            'access_token': token,
            'token_type': 'Bearer'
        })
    response = requests.get(url, auth=auth)

    if response.status_code in (200, 404):
        if response.json():
            content = json.dumps(response.json(), indent=4)
            context['patient_id'] = response.json()['patient']
        else:
            content = {'error': 'problem reading content.'}
    elif response.status_code == 403:
        content = {'error': 'No read capability'}
        content = response.content
    else:
        content = response.content

    context['remote_status_code'] = response.status_code
    context['remote_content'] = content
    context['url'] = url
    return render(request, 'bbof.html', context)


@login_required
def bbof_get_patient(request, patient_id=None):
    context = {'name': 'Blue Button on FHIR'}
    context['patient_id'] = patient_id
    urls = build_fhir_urls(patient_id)

    # first we get the token used to login
    token = request.user.social_auth.get(provider='oauth2io').access_token
    auth = OAuth2(
        settings.SOCIAL_AUTH_OAUTH2IO_KEY,
        token={
            'access_token': token,
            'token_type': 'Bearer'
        })
    # next we call the remote api
    url = urls['patient']

    logging.debug("calling FHIR Service with %s" % url)

    response = requests.get(url, auth=auth)

    if response.status_code in (200, 404):
        if response.json():
            content = json.dumps(response.json(), indent=4)
            context = get_resourceType(context, response.json())

        else:
            content = {'error': 'problem reading content.'}
    elif response.status_code == 403:
        content = {'error': 'No read capability'}
        content = response.content
    else:
        content = response.content

    context['remote_status_code'] = response.status_code
    context['remote_content'] = content
    context['url'] = url
    context['patient'] = patient_id
    return render(request, 'bbof.html', context)


@login_required
def bbof_get_eob(request, patient_id=None):
    context = {'name': 'Blue Button on FHIR'}
    context['patient_id'] = patient_id

    # print("url called: %s" % request.get_full_path())

    # first we get the token used to login
    token = request.user.social_auth.get(provider='oauth2io').access_token
    auth = OAuth2(
        settings.SOCIAL_AUTH_OAUTH2IO_KEY,
        token={
            'access_token': token,
            'token_type': 'Bearer'
        })
    urls = build_fhir_urls(patient_id)

    this_url = urls['eob']
    qp = query_params(request.get_full_path())
    pp = paging_params(qp)

    url_qp = query_params(this_url)
    if url_qp:
        this_url += "&%s" % dict_to_urlencode(pp)
    else:
        this_url += "?%s" % dict_to_urlencode(pp)

    response = requests.get(this_url, auth=auth)

    if response.status_code in (200, 404):
        if response.json():
            content = json.dumps(response.json(), indent=4)
            context = get_links(request, context, response.json())
            context = get_resourceType(context, response.json())

        else:
            content = {'error': 'problem reading content.'}

    elif response.status_code == 403:
        content = {'error': 'No read capability'}
        content = response.content

    else:
        content = response.json()

    # print(content)

    context['remote_status_code'] = response.status_code
    context['remote_content'] = content

    return render(request, 'bbof.html', context)


@login_required
def bbof_get_coverage(request, patient_id=None):
    context = {'name': 'Blue Button on FHIR'}
    context['patient_id'] = patient_id
    # first we get the token used to login
    token = request.user.social_auth.get(provider='oauth2io').access_token
    auth = OAuth2(
        settings.SOCIAL_AUTH_OAUTH2IO_KEY,
        token={
            'access_token': token,
            'token_type': 'Bearer'
        })
    urls = build_fhir_urls(patient_id)
    this_url = urls['coverage']
    qp = query_params(request.get_full_path())
    pp = paging_params(qp)

    url_qp = query_params(this_url)
    if url_qp:
        this_url += "&%s" % dict_to_urlencode(pp)
    else:
        this_url += "?%s" % dict_to_urlencode(pp)

    response = requests.get(this_url, auth=auth)

    if response.status_code in (200, 404):
        if response.json():
            content = json.dumps(response.json(), indent=4)
            context = get_links(request, context, response.json())
            context = get_resourceType(context, response.json())
        else:
            content = {'error': 'problem reading content.'}

    elif response.status_code == 403:
        content = {'error': 'No read capability'}
        content = response.content
    else:
        content = response.json()
    context['remote_status_code'] = response.status_code
    context['remote_content'] = content
    return render(request, 'bbof.html', context)


@login_required
def bbof_get_fhir(request, resource_type, patient):
    context = {'name': 'Blue Button on FHIR'}
    context['patient_id'] = patient

    # first we get the token used to login
    token = request.user.social_auth.get(provider='oauth2io').access_token
    auth = OAuth2(
        settings.SOCIAL_AUTH_OAUTH2IO_KEY,
        token={
            'access_token': token,
            'token_type': 'Bearer'
        })
    # next we call the remote api
    endpoint = '/v1/fhir/%s/?%s=59b99cd030c49e0001481f44&_format=json' % (
        resource_type, patient)

    url = urljoin(
        getattr(settings, 'OAUTH2IO_HOST',
                "https://sandbox.bluebutton.cms.gov"), endpoint)
    # % (request.user.username)

    logging.debug("calling FHIR Service with %s" % url)

    response = requests.get(url, auth=auth)

    if response.status_code in (200, 404):
        if response.json():
            content = json.dumps(response.json(), indent=4)
        else:
            content = {'error': 'problem reading content.'}
    elif response.status_code == 403:
        content = {'error': 'No read capability'}
        content = response.content
    elif response.status_code <= 500:
        content = {
            'error': '500 Error from the server.',
            'status_code': response.status_code
        }
        content = response.content
    else:
        content = response.content

    context['remote_status_code'] = response.status_code
    context['remote_content'] = content
    context['patient'] = patient
    return render(request, 'bbof.html', context)


# @login_required
# def fhir_paging(request, direction="next", url=None):
#     # handle paging


def get_resourceType(context, response_json):
    """
    get the resourceType to add to Context

    """
    if 'resourceType' in response_json:
        rt = response_json['resourceType']
    else:
        rt = ""

    context['resourceType'] = rt

    if rt.lower() == "bundle":
        if 'entry' in response_json:
            if 'resource' in response_json['entry'][0]:
                if 'resourceType' in response_json['entry'][0]['resource']:
                    context['resourceType'] += ":" + response_json['entry'][0]['resource']['resourceType']

    return context


def get_links(request, context, response_json):
    """
    handle the json bundle
    :param context:
    :param response_json:
    :return:
    """

    context['same_page'] = False
    context['next_page'] = False
    context['prev_page'] = False
    context['last_page'] = False

    context['same_page_url'] = ""
    context['next_page_url'] = ""
    context['prev_page_url'] = ""
    context['last_page_url'] = ""

    path = request.get_full_path()

    if 'link' in response_json:
        for link_item in response_json['link']:
            qd = query_params(link_item['url'])
            pd = merge_query(qd, paging_params(qd))

            if link_item['relation'] == "self":
                context['same_page'] = True
                context['same_page_url'] = "%s?%s" % (path,
                                                      dict_to_urlencode(pd))
            elif link_item['relation'] == "next":
                context['next_page'] = True
                context['next_page_url'] = "%s?%s" % (path,
                                                      dict_to_urlencode(pd))
            elif link_item['relation'] == "previous":
                context['prev_page'] = True
                context['prev_page_url'] = "%s?%s" % (path,
                                                      dict_to_urlencode(pd))
            elif link_item['relation'] == "last":
                context['last_page'] = True
                context['last_page_url'] = "%s?%s" % (path,
                                                      dict_to_urlencode(pd))

    return context


def query_params(url=""):
    """
    Get url parameters from url
    :param url:
    :return:
    """

    u = urlparse(url)

    qd = dict(parse_qsl(u.query))

    return qd


def paging_params(qd={}):
    """
    get the paging parameters from the query parameter dict
    :param qd: [dict]
    :return:
    """

    paging_dict = {}
    if 'startIndex' in qd:
        paging_dict['startIndex'] = qd['startIndex']
    if 'count' in qd:
        paging_dict['count'] = qd['count']

    return paging_dict


def dict_to_urlencode(d={}):
    """
    convert dict to urlencode string
    :param d:
    :return: du
    """

    if d:
        du = urlencode(d)
        return du
    else:
        return


def merge_query(query={}, paging={}):
    """
    merge the query parameters passed in with the paging parameters
    :param query:
    :param paging:
    :return: new_query
    """

    new_query = query

    if paging:
        for item, value in paging.items():
            new_query[item] = value

    return new_query
