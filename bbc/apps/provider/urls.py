from __future__ import absolute_import
from __future__ import unicode_literals

from django.conf.urls import patterns, include, url

from .views import *


urlpatterns = patterns('',
    url(r'^pjson/push$', pjson_provider_push,  name="pjson_provider_push"),
    url(r'^fhir/practitioner/push$', fhir_practitioner_push,
        name="fhir_practitioner_push"),
    url(r'^fhir/organization/push$', fhir_organization_push,
        name="fhir_organization_push"),
    url(r'^fhir/practitioner/update$', fhir_practitioner_update,
        name="fhir_practitioner_update"),
    url(r'^fhir/organization/update$', fhir_organization_update,
        name="fhir_organization_update"),
    url(r'^fetch-practitioner$',  fetch_practitioner,
        name="fetch_practitioner"),
    url(r'^update-practitioner/(?P<npi>[^/]+)$',  update_practitioner,
        name="update_practitioner"),
    url(r'^address/update/(?P<id>[^/]+)$',  update_address,
        name="update_address"),
    url(r'^address/delete/(?P<id>[^/]+)$',  delete_address,
        name="delete_address"),
    url(r'^address/create/(?P<npi>[^/]+)$',  create_address,
        name="create_address"),
    url(r'^affiliation/update/(?P<id>[^/]+)$',  update_affiliation,
        name="update_affiliation"),
    url(r'^affiliation/delete/(?P<id>[^/]+)$',  delete_affiliation,
        name="delete_affiliation"),
    url(r'^affiliation/create/(?P<npi>[^/]+)$',  create_affiliation,
        name="create_affiliation"),
    url(r'^submit-to-fhir-server/(?P<npi>[^/]+)$',  submit_to_fhir,
        name="submit_to_fhir"),
)
