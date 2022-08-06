# Generated by Django 4.0.5 on 2022-08-06 10:57

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('latitude', models.FloatField(validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)])),
                ('longitude', models.FloatField(validators=[django.core.validators.MinValueValidator(-90), django.core.validators.MaxValueValidator(90)])),
                ('validity', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
