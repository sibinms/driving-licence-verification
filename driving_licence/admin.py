from django.contrib import admin

# Register your models here.
from driving_licence.models import DrivingLicence


@admin.register(DrivingLicence)
class DrivingLicenceAdminView(admin.ModelAdmin):
    fieldsets = (
        (
            'User Information', {
                'fields': ('user', 'date_of_birth', 'profile', 'address')
            }
        ),
        (
            'Licence Information', {
                'fields': ('license_id', 'driving_licence', 'expiry_date', 'issued_by', 'issued_date', 'other_details')
            }
        ),
        (
            'Authenticity', {
                'fields': ('authenticity_score', 'is_valid')
            }

        ),
        (
            'Timestamp', {
                'fields': ('created_at', 'updated_at', 'task_scheduled')
            }
        )
    )
    list_display = ('user', 'license_id', 'expiry_date', 'is_valid')
    readonly_fields = ('created_at', 'updated_at')
