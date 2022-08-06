from django.urls import path
from common.views import home

app_name = 'common'

urlpatterns = [
    path('', home, name='home'),
]