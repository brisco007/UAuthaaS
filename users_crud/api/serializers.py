from rest_framework.serializers import ModelSerializer
from users_crud.models import DeviceType, Device, UserProfil


class UserProfilSerializer(ModelSerializer):
    class Meta:
        model = UserProfil
        fields = '__all__'


class DeviceTypeSerializer(ModelSerializer):
    class Meta:
        model = DeviceType
        fields = '__all__'


class DeviceSerializer(ModelSerializer):
    class Meta:
        model = Device
        exludes = ('deleted', )
