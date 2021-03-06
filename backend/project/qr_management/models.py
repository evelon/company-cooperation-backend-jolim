import uuid
from django.db import models
from django.contrib.auth import get_user_model


class Location(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL)
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    validity = models.BooleanField(default=True, null=False)
