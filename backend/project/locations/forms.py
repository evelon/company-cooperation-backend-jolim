from django.forms import ModelForm
from locations.models import Location


class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = ['latitude', 'longitude']
