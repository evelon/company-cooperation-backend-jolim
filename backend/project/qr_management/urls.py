from qr_management import views
from django.urls import path

urlpatterns = [
    path('locations', views.LocationAPIView.as_view()),
    path('locations/random-delete', views.test_delete),
    path('locations/<int:location_id>', views.LocationIdAPIView.as_view()),
]