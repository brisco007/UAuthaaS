from rest_framework.serializers import ModelSerializer, Serializer, CharField
from users_crud.models import DeviceType, Device, UserProfil
from keycloak.exceptions import KeycloakError
import ast

# keycloak error

class KeyCloakErrorSerializer:

    def __init__(self, error):
        self.error = error

    @property
    def data(self):
        data = {
            "response_code": self.error.response_code,
            "error_message": ast.literal_eval(self.error.error_message.decode('UTF-8')),
        }
        if getattr(self.error, "message_body", None) is not None:
            data["message_body"] = ast.literal_eval(self.error.message_body.decode('UTF-8'))
        return data

# login


class LoginUserSerializer(Serializer):
    username = CharField()
    password = CharField()

    def validate(self, data):
        return data


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
