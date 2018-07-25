#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

"""
Project: bbc_pd
App: apps.probie
FILE: jpath.py
Created: 7/24/18 9:05 PM

Created by: '@ekivemark'
"""

import json
from django import template
from ..fhirpath import get_jpath

register = template.Library()


@register.filter('jpath')
def jpath(jdict, j_path=""):
    """
    add to template: {% load jpath %}
    example: {% card_item|jpath:path_string %}
    :param jdict:
    :param j_path
    :return result:
    """

    if isinstance(jdict, str):

        json_dict = json.loads(jdict)
        result = get_jpath(j_path, json_dict)
        return result
    else:
        pass
    return
