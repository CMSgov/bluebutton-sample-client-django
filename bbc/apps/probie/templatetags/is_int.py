#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

"""
Project: bbc_pd
App: apps.probie
FILE: is_int.py
Created: 7/16/18 9:05 PM

Created by: '@ekivemark'
"""

from django import template

register = template.Library()


@register.filter('is_int')
def startswith(text):
    """
    add to template: {% load is_int %}
    example: <li{% if variable|is_int %} class="number"{% endif %}>
    :param text:
    :return: True | False
    """

    num_text = text.isdigit()

    if num_text:
        return True
    else:
        return False
