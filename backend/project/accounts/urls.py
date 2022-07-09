from django.urls import path
from .views import (
    CreateUserAPIView,
    ResendVerificationAPIView,
    VerifyEmailAPIView,
    DecoratedTokenObtainPairView,
    DecoratedTokenVerifyView,
    DecoratedTokenRefreshView,
)


urlpatterns = [
    path('register', CreateUserAPIView.as_view(), name='user_create'),
    path('resend', ResendVerificationAPIView.as_view(), name='verification_resend'),
    path('verify', VerifyEmailAPIView.as_view(), name='email_verify'),
    path('token', DecoratedTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', DecoratedTokenRefreshView.as_view(), name='token_refresh'),
]
