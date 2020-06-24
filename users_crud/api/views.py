from rest_framework import viewsets, permissions, response, generics, status
from users_crud.api.serializers import (DeviceSerializer,  DeviceTypeSerializer, UserProfilSerializer,
                                        LoginUserSerializer, KeyCloakErrorSerializer)
from django.shortcuts import get_object_or_404
from users_crud.models import Device, UserProfil, DeviceType
from users_crud import keycloak_web, keycloak_admin
from keycloak.exceptions import KeycloakError


class LoginAPI(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            try:
                token = keycloak_web.token(data['username'], data["password"])
                return response.Response({
                    "token": token
                })
            except KeycloakError as e:
                error_data = KeyCloakErrorSerializer(e).data
                return response.Response(
                    error_data, status=error_data["response_code"])
        else:
            return response.Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)


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


class SignupAPI(generics.GenericAPIView):
    """ create users .. following representation designed by keyclaok """

    def post(self, request, *args, **kwargs):
        credentials = request.data.copy()
        credentials['enabled'] = True
        try:
            new_user = keycloak_admin.create_user(payload=credentials)
            profile = UserProfil.objects.get_or_create(keycloak_id=new_user)
            profile_data = UserProfilSerializer(profile).data
            response_data = {}
            response_data['id'] = new_user
            response_data['profile'] = profile_data

            return response.Response(response_data, status=status.HTTP_201_CREATED)

        except KeycloakError as e:
            error_data = KeyCloakErrorSerializer(e).data
            return response.Response(
                error_data, status=error_data["response_code"])

