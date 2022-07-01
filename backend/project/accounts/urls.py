from django.urls import path
from .views import CreateUserAPIView

urlpatterns = [
    path('users', CreateUserAPIView.as_view(), name='create user')
]
