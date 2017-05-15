#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.decorators.http import  require_GET
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _


@login_required
def my_logout(request):
    logout(request)
    messages.success(request, _("You have been logged out."))
    return HttpResponseRedirect(reverse('login'))

@require_GET    
def my_login(request):
    #this is a GET
    return render(request,'login.html', {'PROPRIETARY_BACKEND_NAME': settings.PROPRIETARY_BACKEND_NAME})



