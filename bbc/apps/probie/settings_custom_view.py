#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

"""
Project: bbc_pd
App: apps.probie
FILE: settings.py
Created: 7/18/18 4:27 PM

Created by: '@ekivemark'

Store the CUSTOM_VIEW list

The CUSTOM_VIEW list is used to create Custom Json resource views

"""

CUSTOM_VIEW = [
    {'view': 'Patient',
     'display_title': '',
     'pathName': 'resourceType'},
    {'view': 'Patient',
     'display_title': 'Patient Identifier',
     'pathName': 'identifier.0.value'},
    {'view': 'Patient',
     'display_title': 'Patient Name',
     'pathName': 'name.0.given.0'},
    {'view': 'Patient',
     'display_title': 'Patient Last Name',
     'pathName': 'name.0.family'},
    {'view': 'Patient',
     'display_title': 'Date of Birth',
     'pathName': 'birthDate'},
    {'view': 'Patient',
     'display_title': 'Patient Zip Code',
     'pathName': 'address.0.postalCode'},
    {'view': "Patient",
     "display_title": "State",
     "pathName": "address.0.state"},
    {'view': 'Coverage',
     'display_title': '',
     'pathName': 'entry.0.resource.resourceType'},
    {'view': 'Coverage',
     'display_title': '',
     'pathName': 'entry.0.resource.status'},
    {'view': 'Coverage',
     'display_title': 'Medicare Plan',
     'pathName': 'entry.0.resource.type.coding.0.code'},
    {'view': 'Coverage',
     'display_title': '',
     'pathName': 'entry.1.resource.status'},
    {'view': 'Coverage',
     'display_title': 'Medicare Plan',
     'pathName': 'entry.1.resource.type.coding.0.code'},
    {'view': 'Coverage',
     'display_title': '',
     'pathName': 'entry.2.resource.status'},
    {'view': 'Coverage',
     'display_title': 'Medicare Plan',
     'pathName': 'entry.2.resource.type.coding.0.code'},
    {'view': 'Coverage',
     'display_title': 'Last updated',
     'pathName': 'meta.lastUpdated'},
    {'view': 'Coverage',
     'display_title': 'Insurance Plans',
     'pathName': 'entry'},

]
