from rest_framework import serializers
from .models import LocationQrCode

class LocationQrCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationQrCode
        fields = '__all__'