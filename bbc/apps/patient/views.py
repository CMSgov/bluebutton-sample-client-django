from __future__ import absolute_import
from __future__ import unicode_literals

import json

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

@login_required
def bbof_pull_me(request):
    context = {'name': 'Blue Button on FHIR'}
    # first we get the token used to login
    token = request.user.social_auth.get(provider=settings.PROPRIETARY_BACKEND_NAME).access_token
    auth = OAuth2(settings.SOCIAL_AUTH_MYOAUTH_KEY,
                  token={'access_token': token, 'token_type': 'Bearer'})
    # next we call the remote api
    url = urljoin(settings.HHS_OAUTH_URL, '/monfhir/oauth2/Patient/5863c9705170aa056735d27d')
    print(url)
    response = requests.get(url, auth=auth)
    print(request.path)
    
    if response.status_code in (200, 404):
        content = response.json()
    elif response.status_code == 403:
        content = {'error': 'No read capability'}
    else:
        content = response.json()
    
    print(content)
    
    context['remote_status_code'] = response.status_code
    context['remote_content'] = content
    return render(request, 'bbof.html', context)

@login_required
def djmongo_read(request):
    context = {'name': 'Djmongo OAuth2 Read Test'}
    # first we get the token used to login
    token = request.user.social_auth.get(provider=settings.PROPRIETARY_BACKEND_NAME).access_token
    auth = OAuth2(settings.SOCIAL_AUTH_MYOAUTH_KEY,
                  token={'access_token': token, 'token_type': 'Bearer'})
    # next we call the remote api
    url = urljoin(settings.HHS_OAUTH_URL, 	'/djm/search/api/oauth2/nppes/pjson/pjson2.json')
    response = requests.get(url, auth=auth)
    if response.status_code in (200, 404):
        content = response.json()
    elif response.status_code == 403:
        content = {'error': 'No read capability'}
    else:
        content = response.json()
    
    print(content)
    
    context['remote_status_code'] = response.status_code
    context['remote_content'] = content
    return render(request, 'bbof.html', context)


@login_required
def djmongo_write(request):
    context = {'name': 'Djmongo OAuth2 Write Test'}
    # first we get the token used to login
    token = request.user.social_auth.get(provider=settings.PROPRIETARY_BACKEND_NAME).access_token
    auth = OAuth2(settings.SOCIAL_AUTH_MYOAUTH_KEY,
                  token={'access_token': token, 'token_type': 'Bearer'})
    # next we call the remote api
    url = urljoin(settings.HHS_OAUTH_URL, 	'/djm/write/api/oauth2/reassignments')
    print(url)
    response = requests.get(url, auth=auth)
    json_data = json.loads("""{"hello": "venus"}""",
                            object_pairs_hook=OrderedDict)
    response = requests.post(url, auth=auth, json=json_data)
    if response.status_code == 200:
         content = response.text # json()
    elif response.status_code == 403:
         content = {'error': 'no write capability'}
    else:
         content = {'error': 'server error'}
    context['remote_status_code'] = response.status_code
    context['remote_content'] = content
    return render(request, 'response.html', context)
    



