from rest_framework import viewsets, permissions, response, generics, status
from users_crud.api.serializers import (DeviceSerializer,  DeviceTypeSerializer, UserProfilSerializer,
                                        LoginUserSerializer, KeyCloakErrorSerializer)
from django.shortcuts import get_object_or_404
from users_crud.models import Device, UserProfil, DeviceType
from users_crud import keycloak_web, keycloak_admin
from keycloak.exceptions import KeycloakError


def keycloak_error_response(error):
    error_data = KeyCloakErrorSerializer(error).data
    return response.Response(error_data, status=error_data["response_code"])


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
        credentials['emailVerified'] = True
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


class UserList(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        params = self.request.query_params.copy()
        try:
            users = keycloak_admin.get_users(params)
            for user in users:
                profile = UserProfil.objects.get_or_create(keycloak_id = user['id'])
                user['profile'] = UserProfilSerializer(profile).data
            return response.Response(users, status=status.HTTP_200_OK)
        except KeycloakError as e:
            return keycloak_error_response(e)


class RefreshToken(generics.GenericAPIView):

    def post(self , request, *args, **kwargs):
        token = request.data.get('refresh_token' , None)

        if not token :
            response.Response({'message' : 'Refresh Token attendu'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            new_token = keycloak_web.refresh_token(token)
            return response.Response(new_token, status=status.HTTP_200_OK)
        except KeycloakError as e:
            return keycloak_error_response(e)

class LogoutAPI(generics.GenericAPIView):

    def post(self , request , *args , **kwargs):
        refresh_token = request.data.get('refresh_token' , None)

        if not refresh_token :
            response.Response({'message' : 'Refresh Token attendu'}, status=status.HTTP_400_BAD_REQUEST)

        try :
            keycloak_web.logout(refresh_token)
            return response.Response({},status=status.HTTP_200_OK)
        except KeycloakError as e:
            return keycloak_error_response(e)

class SingleUserAPI(generics.GenericAPIView):
    lookup_field = 'pk'

    def delete(self , request, *args, **kwargs):
        pk = kwargs['pk']
        try:
            result = keycloak_admin.delete_user(pk)
            return response.Response(result,status=status.HTTP_202_ACCEPTED)
        except KeycloakError as e:
            return keycloak_error_response(e)

    def put(self , request , *args , **kwargs):
        pk = kwargs['pk']
        data = request.data.copy()
        try :
            result = keycloak_admin.update_user(pk , data)
            return response.Response(result,status=status.HTTP_202_ACCEPTED)
        except KeycloakError as e:
            return keycloak_error_response(e)

    def get(self , request , *args , **kwargs):
        return response.Response(request.authUser , status=status.HTTP_200_OK)


class SetPasswordApi(generics.GenericAPIView):

    def post(self , request, *args, **kwargs):
        new_password = request.data.get('password' , None)

        if not new_password :

            response.Response({'password' : 'Nouveau Mot de passe attendu'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            result = keycloak_admin.set_user_password(request.authUser['sub'] , new_password)
            return response.Response(result, status=status.HTTP_200_OK)
        except KeycloakError as e:
            return keycloak_error_response(e)
        
        
        