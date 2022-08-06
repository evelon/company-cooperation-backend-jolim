import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Location(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    latitude = models.FloatField(null=False, validators=[MinValueValidator(-180), MaxValueValidator(180)])
    longitude = models.FloatField(null=False, validators=[MinValueValidator(-90), MaxValueValidator(90)])
    validity = models.BooleanField(default=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
