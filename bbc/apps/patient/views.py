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

logger = logging.getLogger('hhs_server.%s' % __name__)


@login_required
def bbof_get_eob(request):
    context = {'name': 'Blue Button on FHIR'}
    # first we get the token used to login
    token = request.user.social_auth.get(provider='oauth2io').access_token
<<<<<<< HEAD
=======

>>>>>>> 535784fa8d78fd14dd8bb4c8a1e6eb815402bfba
    auth = OAuth2(settings.SOCIAL_AUTH_OAUTH2IO_KEY,
                  token={'access_token': token, 'token_type': 'Bearer'})

    # now we construct the url
    url = build_url('/ExplanationOfBenefit/')

    # next we call the remote api
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
        content = response.json()

    # print(content)

    context['remote_status_code'] = response.status_code
    context['remote_content'] = content
    return render(request, 'bbof.html', context)


@login_required
def bbof_get_coverage(request):
    context = {'name': 'Blue Button on FHIR'}
    # first we get the token used to login
    token = request.user.social_auth.get(provider='oauth2io').access_token
<<<<<<< HEAD
=======

>>>>>>> 535784fa8d78fd14dd8bb4c8a1e6eb815402bfba
    auth = OAuth2(settings.SOCIAL_AUTH_OAUTH2IO_KEY,
                  token={'access_token': token, 'token_type': 'Bearer'})

    # now we construct the url
    url = build_url('/Coverage/?_format=json')

    # next we call the remote api
    # patient = % s? request.user.username
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
        content = response.json()

    # print(content)

    context['remote_status_code'] = response.status_code
    context['remote_content'] = content
    return render(request, 'bbof.html', context)


@login_required
def bbof_get_patient(request):
    context = {'name': 'Blue Button on FHIR'}
    # first we get the token used to login
    token = request.user.social_auth.get(provider='oauth2io').access_token
<<<<<<< HEAD
=======

>>>>>>> 535784fa8d78fd14dd8bb4c8a1e6eb815402bfba
    auth = OAuth2(settings.SOCIAL_AUTH_OAUTH2IO_KEY,
                  token={'access_token': token, 'token_type': 'Bearer'})

    # now we construct the url
    url = build_url('/Patient/?_format=json')

    # % (request.user.username)
    # next we call the remote api
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
    return render(request, 'bbof.html', context)


@login_required
def djmongo_read(request):
    context = {'name': 'Djmongo OAuth2 Read Test'}
    # first we get the token used to login
    token = request.user.social_auth.get(provider='oauth2io').access_token
    auth = OAuth2(settings.SOCIAL_AUTH_OAUTH2IO_KEY,
                  token={'access_token': token, 'token_type': 'Bearer'})
    # next we call the remote api
    url = urljoin(
        settings.HHS_OAUTH_URL,
        '/djm/search/api/oauth2/nppes/pjson/pjson2.json')
    response = requests.get(url, auth=auth)
    if response.status_code in (200, 404):
        if response.json():
            content = json.dumps(response.json(), indent=4)
        else:
            content = {'error': 'problem reading content.'}

    elif response.status_code == 403:
        content = {'error': 'No read capability'}
    else:
        content = response.json()

    context['remote_status_code'] = response.status_code
    context['remote_content'] = content
    return render(request, 'bbof.html', context)


@login_required
def djmongo_write(request):
    context = {'name': 'Djmongo OAuth2 Write Test'}
    # first we get the token used to login
    token = request.user.social_auth.get(provider='oauth2io').access_token
    auth = OAuth2(settings.SOCIAL_AUTH_OAUTH2IO_KEY,
                  token={'access_token': token, 'token_type': 'Bearer'})
    # next we call the remote api
    url = urljoin(
        settings.HHS_OAUTH_URL,
        '/djm/write/api/oauth2/reassignments')
    response = requests.get(url, auth=auth)
    json_data = json.loads(response.text,
                           object_pairs_hook=OrderedDict)
    response = requests.post(url, auth=auth, json=json_data)
    if response.status_code == 200:
        content = response.text  # json()
    elif response.status_code == 403:
        content = {'error': 'no write capability'}
    else:
        content = {'error': 'server error'}
    context['remote_status_code'] = response.status_code
    context['remote_content'] = content
<<<<<<< HEAD
=======

>>>>>>> 535784fa8d78fd14dd8bb4c8a1e6eb815402bfba
    return render(request, 'response.html', context)


def build_url(path=""):
    """
    construct the url to make the remote call
    :param path:
    :return: url
    """

    base_url = settings.FHIR_HOST
    # print("base=%s" % settings.FHIR_HOST)

    url = base_url + path
    # print("path URL", url)

    return url
