from rest_framework import generics
from django.contrib.auth import get_user_model
from .serializers import RegistrationSerializer
from rest_framework.permissions import AllowAny


class CreateUserAPIView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]
