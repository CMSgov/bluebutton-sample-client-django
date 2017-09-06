#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _

from apps.remotecalls.forms import JsonForm


@login_required
def authenticated_home(request):

    name = _("Authenticated Home")
    # this is a GET
    context = {'name': name,
               'form': JsonForm(),
               }
    return render(request, 'authenticated-home.html', context)


def public_home(request):
    return render(request, 'public-home.html', {})


def home(request):
    if request.user.is_authenticated:
        return authenticated_home(request)
    return public_home(request)
