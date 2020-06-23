from rest_framework import viewsets, permissions, response
from users_crud.api.serializers import DeviceSerializer,  DeviceTypeSerializer, UserProfilSerializer
from django.shortcuts import get_object_or_404
from users_crud.models import Device, UserProfil, DeviceType


class UserProfilView(viewsets.ModelViewSet):
    serializer_class = UserProfilSerializer
    queryset = UserProfil.objects.filter(enabled=True)


class DeviceTypeView(viewsets.ModelViewSet):
    serializer_class = UserProfilSerializer
    queryset = DeviceType.objects.filter()


class DeviceView(viewsets.ModelViewSet):
    serializer_class = DeviceSerializer
    queryset = Device.objects.filter()

    def destroy(self, request, pk):
        obj = get_object_or_404(Device, pk=pk)
        obj.deleted = True
        obj.save()
        data = self.serializer_class(obj).data
        return response.Response(data)

