from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'patient_fhir_id')
    search_fields = ('user', 'name', 'patient_fhir_id')


admin.site.register(UserProfile, UserProfileAdmin)


