from django.db import models
from django.contrib.auth.models import User


class DrivingLicence(models.Model):
    license_id = models.CharField(null=True, blank=True, max_length=250)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='get_driving_licence')
    driving_licence = models.FileField(null=True, blank=True)
    profile = models.FileField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    issued_by = models.CharField(null=True, blank=True, max_length=250)
    issued_date = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True, default="{}")
    other_details = models.TextField(null=True, blank=True, default="{}")
    authenticity_score = models.FloatField(default=0)
    is_valid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True, editable=False)
    task_scheduled = models.BooleanField(default=False)

