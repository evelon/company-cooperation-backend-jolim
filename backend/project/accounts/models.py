from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(_("email address"), blank=False, unique=True)
    is_active = models.BooleanField(_("active"), default=True)
    is_verified = models.BooleanField(_("email verified"), default=False)
    REQUIRED_FIELDS = ["email", "password"]
