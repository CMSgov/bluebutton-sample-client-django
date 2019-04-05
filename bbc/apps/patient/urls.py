from __future__ import absolute_import
from __future__ import unicode_literals
from django.conf.urls import url
from .views import (bbof_get_patient, bbof_get_eob, bbof_get_coverage,
                    bbof_get_fhir)

urlpatterns = [
    url(r'^Patient/',
        bbof_get_patient,
        name="bbof_get_patient"),
    url(r'^fhir-resource//(?P<fhir_resource>[^/]+)$',
        bbof_get_fhir,
        name="bbof_get_fhir"),
    url(r'^ExplanationOfBenefit/',
        bbof_get_eob,
        name="bbof_get_eob"),
    url(r'^ExplanationOfBenefit/', bbof_get_eob, name="bbof_get_eob_search"),
    url(r'^Coverage/',
        bbof_get_coverage,
        name="bbof_get_coverage"),
    url(r'^Coverage/$', bbof_get_coverage, name="bbof_get_coverage"),
]
