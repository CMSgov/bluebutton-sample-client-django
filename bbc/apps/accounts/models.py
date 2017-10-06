#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from __future__ import absolute_import
from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    patient_fhir_id  = models.CharField(max_length=255,
                                         blank=True,
                                         default='')
    
    def __str__(self):
        name = '%s %s (%s)' % (self.user.first_name,
                               self.user.last_name,
                               self.user.username)
        return name

    def name(self):
        return '%s %s (%s)' % (self.user.first_name,
                               self.user.last_name,
                               self.user.username)