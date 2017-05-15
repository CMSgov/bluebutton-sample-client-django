from __future__ import absolute_import
from __future__ import unicode_literals

from django import forms


class JsonForm(forms.Form):
    json = forms.CharField(label='JSON body', max_length=10000, widget=forms.Textarea)
