from django.urls import path
from locations.views import create_location, list_location, delete_location, generate_qrcode

app_name = 'locations'

urlpatterns = [
    path('create/', create_location, name='create'),
    path('list/', list_location, name='list'),
    path('delete/<uuid:location_id>', delete_location, name='delete'),
    path('generate/<uuid:location_id>', generate_qrcode, name='generate'),
]
