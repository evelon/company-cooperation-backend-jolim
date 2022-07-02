from django.urls import path
from .views import (
    CreateUserAPIView,
    # LoginView,
    DecoratedTokenObtainPairView,
    DecoratedTokenVerifyView,
    DecoratedTokenRefreshView,
)


urlpatterns = [
    path('register', CreateUserAPIView.as_view(), name='create_user'),
    # path('login', LoginView.as_view(), name='login')
    path('token', DecoratedTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/verify', DecoratedTokenVerifyView.as_view(), name='token_verify'),
    path('token/refresh', DecoratedTokenRefreshView.as_view(), name='token_refresh'),
]
