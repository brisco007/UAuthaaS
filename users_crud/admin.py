from django.contrib import admin
from users_crud.models import UserProfil , Device , DeviceType

# Register your models here.

admin.site.register(UserProfil)
admin.site.register(Device)
admin.site.register(DeviceType)