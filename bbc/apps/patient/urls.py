from __future__ import absolute_import
from __future__ import unicode_literals
from django.conf.urls import url
from .views import bbof_get_patient, bbof_get_eob, bbof_get_coverage, djmongo_read, djmongo_write


urlpatterns = [
    url(r'^Patient$', bbof_get_patient, name="bbof_get_patient"),
    url(r'^ExplanationOfBenefit$', bbof_get_eob, name="bbof_get_eob"),
    url(r'^Coverage$', bbof_get_coverage, name="bbof_get_coverage"),
    url(r'^djmongo-read$', djmongo_read, name="djmongo_read"),
    url(r'^djmongo-write$', djmongo_write, name="djmongo_write"),

]
