from qr_management import views
from django.urls import path

urlpatterns = [
    path('locations', views.LocationViewSet.as_view({
        'get': 'list',
        'post': 'create',
    })),
    path('locations/<uuid:pk>', views.LocationViewSet.as_view({
        'get': 'retrieve',
        'patch': 'partial_update',
        'delete': 'destroy',
    })),
    path('locations/random', views.RandomLocationAPIView.as_view()),
    path('locations/random-delete', views.RandomLocationDeleteAPIView.as_view())
]