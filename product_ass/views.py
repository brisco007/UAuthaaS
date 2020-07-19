from django.shortcuts import render
from product_ass import serializers
from rest_framework import response , generics , status
from users_crud.api.views import keycloak_error_response
from keycloak.exceptions import KeycloakError
from users_crud.models import Device
from keycloak import KeycloakOpenID, KeycloakAdmin
from django.conf import settings

admin_config = settings.KEYCLOAK_ADMIN_CONFIG

# Create your views here.

class ServicesList(generics.GenericAPIView):

    queryset = Device.objects.all()
    serializer_class = serializers.ServiceSerializer

    def get(self, request, *args, **kwargs): 
        keycloak_admin = KeycloakAdmin(server_url=admin_config['KEYCLOAK_SERVER_URL'],
                               username=admin_config['KEYCLOAK_USERNAME'],
                               password=admin_config['KEYCLOAK_PASSWORD'],
                               realm_name=admin_config['KEYCLOAK_REALM'],
                               verify=True)

        try:
            applications = keycloak_admin.get_clients()
            return response.Response(applications, status=status.HTTP_200_OK)
        except KeycloakError as e:
            print(e.__class__)
            return keycloak_error_response(e)


    def post(self , request , *args , **kwargs):
        """
            https://www.keycloak.org/docs-api/8.0/rest-api/index.html#_clientrepresentation

            fields : 
                bearerOnly
                clientId
                name
                description
                rootUrl
                secret
                ....

        """

        serializer = serializers.ServiceSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data

            try : 
                created_app = keycloak_admin.create_client(payload=data)
                return response.Response(created_app, status=status.HTTP_201_CREATED)
            except KeycloakError as e:
                return keycloak_error_response(e)

        
        else:
            return response.Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
            


    

    