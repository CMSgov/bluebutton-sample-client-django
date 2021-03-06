#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from ..accounts.models import UserProfile
from ..patient.views import build_fhir_urls
__author__ = "Alan Viars"


@login_required
def authenticated_home(request):
    name = _("Authenticated Home")
    profile, g_o_c = UserProfile.objects.get_or_create(user=request.user)
    context = {'name': name, "profile": profile,
               'fhir_urls': build_fhir_urls(profile.patient_fhir_id),
               'patient_id': profile.patient_fhir_id}
    return render(request, 'authenticated-home.html', context)


def public_home(request):
    return render(request, 'public-home.html', {})


def home(request):
    if request.user.is_authenticated:
        return authenticated_home(request)
    return public_home(request)
