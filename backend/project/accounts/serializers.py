from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(min_length=4, max_length=24, validators=[
        UniqueValidator(queryset=get_user_model().objects.all(), message="Username already exists")
    ])
    password = serializers.CharField(min_length=8, max_length=36, write_only=True)
    email = serializers.EmailField(validators=[
        UniqueValidator(queryset=get_user_model().objects.all(), message="email already exists")
    ])

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user

    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email", "password",)
