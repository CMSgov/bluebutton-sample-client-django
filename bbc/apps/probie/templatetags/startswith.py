#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

"""
Project: bbc_pd
App: apps.probie
FILE: startswith.py
Created: 7/16/18 9:05 PM

Created by: '@ekivemark'
"""

from django import template

register = template.Library()


@register.filter('startswith')
def startswith(text, starts):
    """
    add to template: {% load startswith %}
    example: <li{% if request.path|startswith:'/settings/' %} class="active"{% endif %}>
    :param text:
    :param starts:
    :return: True | False
    """

    try:
        basestring
    except NameError:
        basestring = str

    if isinstance(text, basestring):
        return text.startswith(starts)
    return False
