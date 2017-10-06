#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from __future__ import absolute_import
from __future__ import unicode_literals
from ...models import UserProfile


__author__ = "Alan Viars"


def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'oauth2io':
        profile, g_o_c = UserProfile.objects.get_or_create(user=user)
        profile.patient_fhir_id = response.get('patient')
        profile.save()