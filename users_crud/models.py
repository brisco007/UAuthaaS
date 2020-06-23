from django.db import models
import uuid

# Create your models here.


class UserProfil(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profil = models.ImageField(upload_to='profiles')
    enabled = models.BooleanField(default=True)


class DeviceType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(unique=True, blank=False,
                            null=False, max_length=255)


class Device(models.Model):
    deleted = models.BooleanField(default=False)
    owner = models.ForeignKey(to=UserProfil, on_delete=models.SET_NULL , null=True)
    kind = models.ForeignKey(
        to=DeviceType, on_delete=models.SET_NULL, related_name="devices", null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mac_address = models.CharField(
        unique=True, blank=False, null=False, max_length=255)
    model = models.CharField(unique=True, blank=False,
                             null=False, max_length=255)
    description = models.TextField(blank=True)
