from django.shortcuts import render , redirect
from rest_framework import generics, status, response
from rest_framework.permissions import AllowAny
from rest_framework.serializers import Serializer, CharField, ValidationError
from django.conf import settings
from rest_framework.exceptions import NotFound
from django.http.response import JsonResponse
# Create your views here.
from keycloak import KeycloakOpenID
from keycloak.exceptions import KeycloakConnectionError


config = settings.KEYCLOAK_CONFIG
server_url = config['KEYCLOAK_SERVER_URL']
client_id = "token-client"
realm = config['KEYCLOAK_REALM']
#client_secret_key = config['KEYCLOAK_CLIENT_SECRET_KEY']
keycloak = KeycloakOpenID(server_url=server_url,
                          client_id=client_id,
                          realm_name=realm)


class LoginUserSerializer(Serializer):
    username = CharField()
    password = CharField()

    def validate(self, data):
        return data


class SalutView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return response.Response({"new_token": request.authorization_token, "user": request.authUser})


class LoginAPI(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            print(data['username'], data["password"])
            try:
                token = keycloak.token(data['username'], data["password"])
                return response.Response({
                    "token": token
                })
            except KeycloakConnectionError as e:
                # print(e)
                return response.Response({
                    "Erreur": "err"
                })
        else:
            return response.Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)


def redirect_view(request):
    params = request.GET.copy()

    to = params.pop('to', None)

    if not to:
        return JsonResponse({"detail": NotFound.default_detail},
                                 status=NotFound.status_code)

    #params['token'] = request.authorization_token
    return redirect(to=to[0] , permanent=True , **params)