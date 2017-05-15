from __future__ import absolute_import
from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _
import json
from pdt import json_schema_check_fhir
import requests
from .models import Practitioner, Address
from collections import OrderedDict


class PractitionerModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
         super(PractitionerModelForm, self).__init__(*args, **kwargs)
         instance = getattr(self, 'instance', None)
         if instance and instance.pk:
            self.fields['npi'].widget.attrs['readonly'] = True
            self.fields['fhir_id'].widget.attrs['readonly'] = True
            self.fields['first_name'].widget.attrs['required'] = True
            self.fields['last_name'].widget.attrs['required'] = True

    class Meta:
        model = Practitioner
        fields = ('npi','fhir_id','first_name', 'last_name',)



class FetchPractitionerForm(forms.Form):
    npi = forms.CharField(label='NPI', max_length=10,
            help_text =_("Enter a valid NPI"))

    required_css_class = 'required'
    def clean_npi(self):
        npi = self.cleaned_data.get('npi')
        url = "https://registry.npi.io/search/fhir/Practitioner." \
            "json?identifier.value=%s" % (npi)
        response = requests.get(url)
        try:
            jr = json.loads(response.text)

            if 'results' not in jr:
                msg=_("The lookup failed. Invalid response from server")
                raise forms.ValidationError(msg)

            if not jr['results']:
                    msg=_("Invalid NPI")
                    raise forms.ValidationError(msg)
        except ValueError:
            msg=_("The lookup failed. JSON was not returned by the server.")
            raise forms.ValidationError(msg)
        return npi



class AddressForm(forms.Form):
    line_1= forms.CharField(max_length=255)
    line_2  = forms.CharField(max_length=255, required=False)
    city= forms.CharField(max_length=255)
    state= forms.CharField(max_length=2)
    postal_code= forms.CharField(max_length=15)
    country= forms.CharField(max_length=2)
    use  = forms.ChoiceField(choices = (('home','home'),
        ('work','work'),('mailing', 'mailing')))
    required_css_class = 'required'

    def create_fhir_json(self):
        json_fhir_dict = OrderedDict()
        json_fhir_dict['line']=[]
        json_fhir_dict['line'].append(self.cleaned_data.get('line_1'))
        json_fhir_dict['line'].append(self.cleaned_data.get('line_2'))
        json_fhir_dict['city'] = self.cleaned_data.get('city')
        json_fhir_dict['state'] = self.cleaned_data.get('state')
        json_fhir_dict['postalCode'] = self.cleaned_data.get('postal_code')
        json_fhir_dict['country'] = self.cleaned_data.get('country')
        json_fhir_dict['use'] = self.cleaned_data.get('use')
        return json.dumps(json_fhir_dict, indent=4)

class AffiliationForm(forms.Form):
    purpose = forms.ChoiceField(choices =
                                    (('PROVIDER-NETWORK', 'Provider-Network'),
                                    ('MEDICARE-NETWORK', 'Medicare-Network')))
    npi = forms.CharField(max_length=10, label="Organization's NPI (Type 2)")
    endpoint_data_type = forms.ChoiceField(
                choices = (('DIRECT-EMAIL-ADDRESS', 'Direct-Email-Address')),
                required=False)
    endpoint = forms.CharField(max_length=512, required=False)
    required_css_class = 'required'

    def create_fhir_json(self):
        json_fhir_dict = OrderedDict()
        json_fhir_dict['purpose'] = self.cleaned_data.get('purpose')
        json_fhir_dict['npi'] = self.cleaned_data.get('npi')
        json_fhir_dict['endpoint_data_type'] = self.cleaned_data.get('endpoint_data_type)')
        json_fhir_dict['endpoint'] = self.cleaned_data.get('endpoint')

        return json.dumps(json_fhir_dict, indent=4)


class PractitionerHumanForm(forms.Form):
    first_name = forms.CharField(max_length=255)
    last_name  = forms.CharField(max_length=255)


    required_css_class = 'required'


class OrganizationHumanForm(forms.Form):
    organization_name = forms.CharField(max_length=255)

    required_css_class = 'required'



class JsonForm(forms.Form):
    json = forms.CharField(label='JSON body', max_length=10000,
            widget=forms.Textarea,
            help_text =_("This field must contain a JSON object e.g. {}"))

    required_css_class = 'required'


    def clean_json(self):
        jsonf = self.cleaned_data.get('json')

        try:
            j = json.loads(jsonf)
            if type (j) != type({}):
                msg=_("The field does not contain a valid JSON object.")
                raise forms.ValidationError(msg)

        except ValueError:
            msg=_("The field does not contain valid JSON.")
            raise forms.ValidationError(msg)

        return jsonf

class PractitionerForm(forms.Form):
    json = forms.CharField(label='JSON body',
            max_length=10000, widget=forms.Textarea,
            help_text =_("This field must contain a Practitioner" \
                         "FHIR JSON object e.g. {}"))

    required_css_class = 'required'


    def clean_json(self):
        jsonf  = self.cleaned_data.get('json')
        try:
            j = json.loads(jsonf)
            json_pract_result = json_schema_check_fhir.json_schema_check_fhir(
                'Practitioner', jsonf)
            if json_pract_result['errors'] != []:
                msg=_("The field does not contain a valid FHIR Practitioner" \
                      "JSON object: ", json_pract_result['errors'])
                raise forms.ValidationError(msg)

        except ValueError:
            msg=_("The field does not contain valid JSON.")
            raise forms.ValidationError(msg)

        return jsonf

class OrganizationForm(forms.Form):
    json = forms.CharField(label='JSON body', max_length=10000,
            widget=forms.Textarea,
            help_text =_("This field must contain an Organization FHIR JSON \
                         object e.g. {}"))

    required_css_class = 'required'


    def clean_json(self):
        jsonf = self.cleaned_data.get('json')
        try:
            j = json.loads(jsonf)
            json_org_result = json_schema_check_fhir.json_schema_check_fhir(
                                                                'Organization',
                                                                jsonf)
            if json_org_result['errors'] != []:
                msg=_("The field does not contain a valid FHIR Organization \
                      JSON object: ", json_org_result['errors'])
                raise forms.ValidationError(msg)

        except ValueError:
            msg=_("The field does not contain valid JSON.")
            raise forms.ValidationError(msg)

        return jsonf
