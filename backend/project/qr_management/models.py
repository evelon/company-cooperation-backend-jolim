import uuid
from django.db import models
from django.contrib.auth.models import User

class LocationQrCode(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    validity = models.BooleanField(default=True, null=False)