#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

"""
Project: bbc_pd
App: apps.probie
FILE: forms
Created: 7/17/18 3:39 PM

Created by: '@ekivemark'
"""

from django import forms


class getUrlForm(forms.Form):
    """
    get url to fetch
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['url'].widget.attrs.update(size='80')

    url = forms.URLField()


class getCustomViewForm(forms.Form):
    """
    get url to fetch
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['url'].widget.attrs.update(size='80')

    url = forms.URLField()
    custom_view = forms.CharField(max_length=120)
