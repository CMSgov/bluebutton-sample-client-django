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
from django.views.decorators.http import require_POST

import requests
from requests_oauthlib import OAuth2

from .forms import JsonForm


@login_required
def call_read(request):
    context = {'name': 'Authenticated Home'}
    # first we get the token used to login
    token = request.user.social_auth.get(provider='myoauth').access_token
    auth = OAuth2(settings.SOCIAL_AUTH_MYOAUTH_KEY,
                  token={'access_token': token, 'token_type': 'Bearer'})
    # next we call the remote api
    url = urljoin(settings.HHS_OAUTH_URL, '/api/read/')
    response = requests.get(url, auth=auth)
    if response.status_code == 200:
        content = response.json()
    elif response.status_code == 403:
        content = {'error': 'no read capability'}
    else:
        content = {'error': 'server error'}

    context['form'] = JsonForm()
    context['remote_status_code'] = response.status_code
    context['remote_content'] = content
    return render(request, 'authenticated-home.html', context)


@login_required
@require_POST
def call_write(request):
    context = {'name': 'Authenticated Home'}

    if request.method == 'POST':
        form = JsonForm(request.POST)
        if form.is_valid():
            # first we get the token used to login
            token = request.user.social_auth.get(provider='myoauth').access_token
            auth = OAuth2(settings.SOCIAL_AUTH_MYOAUTH_KEY,
                          token={'access_token': token, 'token_type': 'Bearer'})
            # next we call the remote api
            url = urljoin(settings.HHS_OAUTH_URL, '/api/write/')
            json_data = json.loads(form.cleaned_data['json'])
            response = requests.post(url, auth=auth, json=json_data)
            if response.status_code == 200:
                content = response.json()
            elif response.status_code == 403:
                content = {'error': 'no write capability'}
            else:
                content = {'error': 'server error'}
            context['remote_status_code'] = response.status_code
            context['remote_content'] = content
    else:
        form = JsonForm()

    context['form'] = form
    return render(request, 'authenticated-home.html', context)
