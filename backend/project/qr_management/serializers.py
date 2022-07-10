from rest_framework import serializers
from .models import Location
from random import random


class LocationQrCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


def get_random_latitude():
    return (random() - 0.5) * 90


def get_random_longitude():
    return (random() - 0.5) * 180


class RandomLocationSerializer(serializers.ModelSerializer):
    def validate_latitude(self, value):
        if value < -90 or value > 90:
            raise serializers.ValidationError('Latitude is out of range')
        return value

    def validate_longitude(self, value):
        if value < -90 or value > 90:
            raise serializers.ValidationError('Longitude is out of range')
        return value

    def create(self, validated_data):
        location_qr_code = Location(
            latitude=get_random_latitude(),
            longitude=get_random_longitude()
        )
        location_qr_code.save()
        return location_qr_code

    def update(self, instance, validated_data):
        instance.latitude = get_random_latitude()
        instance.longitude = get_random_longitude()
        instance.save()
        return instance

    class Meta:
        model = Location
        fields = '__all__'
        read_only_fields = ['latitude', 'longitude', 'owner', 'validity']


class LocationSerializer(serializers.ModelSerializer):
    def validate_latitude(self, value):
        if value < -90 or value > 90:
            raise serializers.ValidationError('Latitude is out of range')
        return value

    def validate_longitude(self, value):
        if value < -90 or value > 90:
            raise serializers.ValidationError('Longitude is out of range')
        return value

    class Meta:
        model = Location
        fields = '__all__'
        read_only_fields = ['owner', 'validity']