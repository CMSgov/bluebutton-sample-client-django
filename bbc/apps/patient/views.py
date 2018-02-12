from __future__ import absolute_import
from __future__ import unicode_literals
import json

import logging

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from collections import OrderedDict
import requests
from requests_oauthlib import OAuth2


__author__ = "Alan Viars"


def build_fhir_urls(patient_id=None, since_date=None):
    result = {}
    base = getattr( settings, 'FHIR_BASE_ENDPOINT',
            "https://sandbox.bluebutton.cms.gov/v1/fhir/")
    eob_search = urljoin(base, "ExplanationOfBenefit/")
    result['eob_search'] = eob_search
    patient_search = urljoin(base, "Patient/")
    result['patient_search'] = patient_search

    if patient_id:
        result['coverage'] = urljoin(base, "Coverage/?beneficiary=%s" % (patient_id))
        result['eob'] = urljoin(base, "ExplanationOfBenefit/?patient=%s" % (patient_id))
        result['patient'] = urljoin(base, "Patient/%s" % (patient_id))
    return result






@login_required
def bbof_get_userinfo(request):
    context = {'name': 'Get Userinfo'}
    url = getattr( settings, 'USER_INFO_ENDPOINT',
            "https://sandbox.bluebutton.cms.gov/v1/connect/userinfo")
    token = request.user.social_auth.get(provider='oauth2io').access_token
    auth = OAuth2(settings.SOCIAL_AUTH_OAUTH2IO_KEY,
                  token={'access_token': token, 'token_type': 'Bearer'})
    response = requests.get(url, auth=auth)

    if response.status_code in (200, 404):
        if response.json():
            content = json.dumps(response.json(), indent=4)
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
    urls =  build_fhir_urls(patient_id)
    
    # first we get the token used to login
    token = request.user.social_auth.get(provider='oauth2io').access_token
    auth = OAuth2(settings.SOCIAL_AUTH_OAUTH2IO_KEY,
                  token={'access_token': token, 'token_type': 'Bearer'})
    # next we call the remote api
    url = urls['patient']

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
    else:
        content = response.content

    context['remote_status_code'] = response.status_code
    context['remote_content'] = content
    context['url'] = url
    context['pqtient'] = patient_id
    return render(request, 'bbof.html', context)





@login_required
def bbof_get_eob(request, patient_id=None):
    context = {'name': 'Blue Button on FHIR'}
    # first we get the token used to login
    token = request.user.social_auth.get(provider='oauth2io').access_token
    auth = OAuth2(settings.SOCIAL_AUTH_OAUTH2IO_KEY,
                  token={'access_token': token, 'token_type': 'Bearer'})
    urls =  build_fhir_urls(patient_id)
    response = requests.get(urls['eob'], auth=auth)

    if response.status_code in (200, 404):
        if response.json():
            content = json.dumps(response.json(), indent=4)
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
    # first we get the token used to login
    token = request.user.social_auth.get(provider='oauth2io').access_token
    auth = OAuth2(settings.SOCIAL_AUTH_OAUTH2IO_KEY,
                  token={'access_token': token, 'token_type': 'Bearer'})
    urls =  build_fhir_urls(patient_id)
    response = requests.get(urls['coverage'], auth=auth)

    if response.status_code in (200, 404):
        if response.json():
            content = json.dumps(response.json(), indent=4)
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
    # first we get the token used to login
    token = request.user.social_auth.get(provider='oauth2io').access_token
    auth = OAuth2(settings.SOCIAL_AUTH_OAUTH2IO_KEY,
                  
                  
                  
                  token={'access_token': token, 'token_type': 'Bearer'})
    # next we call the remote api
    endpoint = '/v1/fhir/%s/?%s=59b99cd030c49e0001481f44&_format=json' % (
        resource_type, patient)

    url = urljoin(
        getattr(
            settings,
            'OAUTH2IO_HOST',
            "https://sandbox.bluebutton.cms.gov"), endpoint)
    print(url)
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
        content = {'error': '500 Error from the server.',
                   'status_code': response.status_code }
        content = response.content
    else:
        content = response.content

    context['remote_status_code'] = response.status_code
    context['remote_content'] = content
    ontext['patient'] = patient
    return render(request, 'bbof.html', context)



