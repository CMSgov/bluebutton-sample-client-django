from django.contrib import admin
from .models import Practitioner, Organization, Address, Affiliation, License, Taxonomy


class PractitionerAdmin(admin.ModelAdmin):
    
    list_display =  ('first_name', 'last_name', 'npi', 'fhir_id')
    search_fields = ('first_name', 'last_name', 'npi' )
    
admin.site.register(Practitioner, PractitionerAdmin)
admin.site.register(Organization)


class AddressAdmin(admin.ModelAdmin):
    
    list_display =  ('npi', 'line_1', 'line_2', 'city', 'state', 'postal_code', 'country', 'use')
    search_fields = ('npi', )


admin.site.register(Address, AddressAdmin)
admin.site.register(Affiliation)
admin.site.register(License)
admin.site.register(Taxonomy)
