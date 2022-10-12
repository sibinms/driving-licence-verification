from rest_framework.serializers import (
    ModelSerializer,
)

from driving_licence.models import DrivingLicence


class DrivingLicenceSerializer(ModelSerializer):
    class Meta:
        model = DrivingLicence
        fields = [
            'license_id',
            'issued_by',
            'issued_date',
            'expiry_date',
            'address',
            'is_valid'
        ]
