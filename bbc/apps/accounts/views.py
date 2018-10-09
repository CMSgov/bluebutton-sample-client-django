#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
# from django.conf import settings
# from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
# from django.http import HttpResponse
# from django.views.decorators.http import require_GET
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
# from requests_oauthlib import OAuth2Session
# import os
# from django.views.decorators.csrf import csrf_exempt, csrf_protect
# from django.views.decorators.cache import never_cache

__author__ = "Alan Viars"


@login_required
def my_logout(request):
    logout(request)
    messages.success(request, _("You have been logged out."))
    return HttpResponseRedirect(reverse('home'))


# @require_GET
# def my_login(request):
#     # this is a GET
#     return render(
#         request, 'login.html', {
#             'PROPRIETARY_BACKEND_NAME': 'myoauth2'})
#
#
# def instagram_login(request):
#     client_id = settings.SOCIAL_AUTH_INSTAGRAM_KEY
#     client_secret = settings.SOCIAL_AUTH_INSTAGRAM_SECRET
#     base_host = "https://api.instagram.com"
#     base_authorization_url = base_host + '/oauth/authorize'
#     token_url = base_host + '/oauth/token'
#     scope = settings.SOCIAL_AUTH_INSTAGRAM_SCOPE
#     redirect_url = "http://localhost:8001" + "/accounts/instagram/redirect"
#     insta = OAuth2Session(client_id, redirect_uri=redirect_url, scope=scope)
#     authorization_url, state = insta.authorization_url(base_authorization_url)
#     request.session[0] = state
#     print("SESSION_STATE", state)
#     return HttpResponseRedirect(authorization_url)
#
#
# @csrf_exempt
# @never_cache
# def instagram_redirect(request):
#     print("BODY", request.body)
#     print("CODE", request.GET.get('code', ''))
#     print("STATE", request.GET.get('state', ''))
#     client_id = settings.SOCIAL_AUTH_INSTAGRAM_KEY
#     client_secret = settings.SOCIAL_AUTH_INSTAGRAM_SECRET
#     base_host = "https://api.instagram.com"
#     base_authorization_url = base_host + '/oauth/authorize'
#     token_url = base_host + '/oauth/token'
#     scope = settings.OAUTH2IO_SCOPE
#     redirect_url = settings.HOSTNAME_URL + "/accounts/instagram/redirect"
#     #print("SESSION STATE 2:", request.session['0'])
#     authorization_response = settings.HOSTNAME_URL + request.get_full_path()
#     print("Authorization response:", authorization_response)
#     insta = OAuth2Session(client_id, redirect_uri=redirect_url, scope=[])
#     print(dir(insta))
#     insta.fetch_token(token_url, client_secret=client_secret,
#                       authorization_response=authorization_response)
#     print(token)
#     return HttpResponse(token)
#
#
# def oauth2io_login(request):
#     os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
#
#     client_id = settings.OAUTH2IO_KEY
#     client_secret = settings.OAUTH2IO_SECRET
#     base_host = settings.OAUTH2IO_HOST
#     redirect_url = settings.HOSTNAME_URL + "/accounts/oauth2io/redirect"
#     authorization_url = base_host + '/o/authorize'
#     token_url = base_host + '/o/token'
#     scope = settings.OAUTH2IO_SCOPE
#     oa2 = OAuth2Session(client_id, redirect_uri=redirect_url, scope=[])
#     authorization_url, state = oa2.authorization_url(authorization_url)
#     request.session[0] = state
#     print("SESSION_STATE", state)
#     return HttpResponseRedirect(authorization_url)
#
#
# @csrf_exempt
# @never_cache
# def oauth2io_redirect(request):
#     os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
#     print("BODY", request.body)
#     print("CODE", request.GET.get('code', ''))
#     client_id = settings.OAUTH2IO_KEY
#     client_secret = settings.OAUTH2IO_SECRET
#     base_host = settings.OAUTH2IO_HOST
#     token_url = base_host + '/o/token'
#     redirect_url = settings.HOSTNAME_URL + "/accounts/oauth2io/redirect"
#     print("SESSION STATE 2:", request.session['0'])
#     authorization_response = settings.HOSTNAME_URL + request.get_full_path()
#     print("Authorization response:", authorization_response)
#     oa2 = OAuth2Session(client_id, scope=[])
#     token = oa2.fetch_token(token_url,
#                             state=request.session['0'],
#                             client_secret=client_secret,
#                             authorization_response=authorization_response)
#     print(token)
#     return HttpResponse(token)
#
#
# def idme_login(request):
#     os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
#     print("IDME Authorization")
#     idme = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
#     authorization_url = idme.authorization_url(authorization_base_url)
#     print(authorization_url)
#     return HttpResponseRedirect(authorization_url[0])
#
#
# def idme_redirect(request):
#     print(request)
#
#
# def okta_login(request):
#     print("Okta Authorization")
#     client_id = '0oabhp13fgETSkKGF0h7'
#     client_secret = 'KiarYxiJep1qszWfx3RoPEFbjMpcpXUmg-eaJhLM'
#     redirect_uri = 'http://localhost:8000/accounts/okta-redirect'
#     authorization_base_url = 'https://dev-841577.oktapreview.com/oauth2/0oabhp13fgETSkKGF0h7/v1/authorize'
#     token_url = 'https://dev-841577.oktapreview.com/oauth2/0oabhp13fgETSkKGF0h7/v1/token'
#     attributes_url = 'https://dev-841577.oktapreview.com/oauth2/0oabhp13fgETSkKGF0h7/v1/userinfo'
#     scope = ['openid', 'profile']
#     idme = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
#     authorization_url = idme.authorization_url(authorization_base_url)
#     print(authorization_url)
#     return HttpResponseRedirect(authorization_url[0])
#
#
# def okta_redirect(request):
#     print(request)
#     return HttpResponse(request)
