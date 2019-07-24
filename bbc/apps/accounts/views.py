#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _


__author__ = "Alan Viars"


@login_required
def my_logout(request):
    # applying fix for non-admin user
    removed = False
    u = request.user
    u_n = request.user.username

    if not u.is_staff:
        # remove this non-staff user account on logout
        u.delete()
        removed = True

    logout(request)
    if removed:
        messages.success(request, _("Temporary account removed for %s." % u_n))
    else:
        messages.success(request, _("You have been logged out."))
    return HttpResponseRedirect(reverse('home'))
