from __future__ import absolute_import
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
import json
from django.contrib.auth.models import User
from collections import OrderedDict
from .utils import get_practitioner, get_pecos_individual_affliliation


@python_2_unicode_compatible
class Address(models.Model):
    npi                     = models.CharField(max_length=10, default="",
                                               blank=True)
    fhir_json_snipit        = models.TextField(max_length=2000, default="")


    def __str__(self):
        try:
          j = json.loads(self.fhir_json_snipit)
          address=""
          for l in j['line']:
            address = address + l + " "

          address = address + " " + j['city'] + " " + j['state'] + " " \
                    +  j['postalCode'] + " " +  j['country'] + \
                    " (" + j['use'] + ")"
          return address

        except ValueError:
            return "%s" % (self.id)
        except:
            return "%s" % (self.id)
    def as_dict(self):
        result = {}
        try:
            j = json.loads(self.fhir_json_snipit)
            result['line_1'] = j['line'][0]
            result['line_2'] = j['line'][1]
            result['city'] = j['city']
            result['state'] = j['state']
            result['postal_code'] = j['postalCode']
            result['use'] = j['use']
            result['country'] = j['country']
            return result
        except:
            return {}


    def line_1(self):
        try:
            j = json.loads(self.fhir_json_snipit)
            line = j['line'][0]
            return line
        except:
             return ""
    def line_2(self):
        try:
            j = json.loads(self.fhir_json_snipit)
            line = j['line'][1]
            return line
        except:
             return ""



    def city(self):
        try:
            j = json.loads(self.fhir_json_snipit)
            return j['city']
        except:
            return ""

    def state(self):
        try:
            j = json.loads(self.fhir_json_snipit)
            return j['state']
        except:
            return ""


    def postal_code(self):
        try:
            j = json.loads(self.fhir_json_snipit)
            return j['postalCode']
        except:
            return ""
    def country(self):
        try:
            j = json.loads(self.fhir_json_snipit)
            return j['country']
        except:
            return ""

    def use(self):
        try:
            j = json.loads(self.fhir_json_snipit)
            return j['use']
        except:
            return ""



@python_2_unicode_compatible
class Taxonomy(models.Model):
    npi                     = models.CharField(max_length=10, default="",
                                               blank=True)
    fhir_json_snipit        = models.TextField(max_length=2000, default="")


    def __str__(self):
        return "%s" % (self.id)

@python_2_unicode_compatible
class License(models.Model):
    npi                     = models.CharField(max_length=10, default="",
                                               blank=True)
    fhir_json_snipit        = models.TextField(max_length=2000, default="")


    def __str__(self):
        return "%s" % (self.id)

@python_2_unicode_compatible
class Affiliation(models.Model):
    npi = models.CharField(max_length=10, default="",
                                               blank=True)
    fhir_json_snipit = models.TextField(max_length=2000, default="")

    def __str__(self):
        return "%s" % (self.npi)
    # 
    # def as_dict(self):
    #     result = {}
    #     try:
    #         j = json.loads(self.fhir_json_snipit)
    #         return result
    #     except:
    #         return {}
    # 
    # def npi(self):
    #     try:
    #         j = json.loads(self.fhir_json_snipit)
    #         return j['npi']
    #     except:
    #         return ""



@python_2_unicode_compatible
class Practitioner(models.Model):
    user                    = models.ForeignKey(User, blank= True, null=True)
    npi                     = models.CharField(max_length=10, default="",
                                               unique=True,
                                              )
    fhir_id                 = models.CharField(max_length=24, default="",
                                               unique=True,
                                                verbose_name="FHIR ID")
    first_name              = models.CharField(max_length=256, default="",
                                               blank=True)
    last_name               = models.CharField(max_length=256, default="",
                                               blank =True)
    doing_business_as       = models.CharField(max_length=256, default="",
                                               blank=True)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    def name_to_fhir(self):
        names =[ ]
        name = OrderedDict()
        name['given'] = self.first_name
        name['family'] = self.last_name
        names.append(name)
        return names


    def to_fhir(self):
        pfhir = OrderedDict()
        pfhir.update(get_practitioner(self.npi))
        pfhir.update(get_pecos_individual_affliliation(self.npi))

        addresses =  Address.objects.filter(npi=self.npi)
        address= []
        for a in addresses:
            address.append(json.loads(a.fhir_json_snipit))

        affiliations =  Affiliation.objects.filter(npi=self.npi)
        affiliation= []
        for a in affiliations:
            affiliation.append(json.loads(a.fhir_json_snipit))



        #Override our changes
        pfhir['address'] = address
        pfhir['affiliation'] = affiliation
        pfhir['name']    = self.name_to_fhir()
        #Bump the version
        pfhir['meta']['version'] = pfhir['meta']['version'] + 1
        return pfhir


    def to_fhir_json(self):
        return json.dumps(self.to_fhir(), indent=4)



@python_2_unicode_compatible
class Organization(models.Model):
    npi                     = models.CharField(max_length=10, default="")
    fhir_id                 = models.CharField(max_length=24, default="")
    organization_name       = models.CharField(max_length=256, default="")
    doing_business_as       = models.CharField(max_length=256, default="")

    def __str__(self):
        return "%s" % (self.organization_name)
