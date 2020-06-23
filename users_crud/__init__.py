from keycloak import KeycloakOpenID, KeycloakAdmin
from django.conf import settings


web_config = settings.KEYCLOAK_WEB_CONFIG

admin_config = settings.KEYCLOAK_ADMIN_CONFIG


keycloak_web = KeycloakOpenID(server_url=web_config['KEYCLOAK_SERVER_URL'],
                              client_id=web_config['KEYCLOAK_CLIENT_ID'],
                              realm_name=web_config['KEYCLOAK_REALM'])


keycloak_admin = KeycloakAdmin(server_url=admin_config['KEYCLOAK_SERVER_URL'],
                               username=admin_config['KEYCLOAK_USERNAME'],
                               password=admin_config['KEYCLOAK_PASSWORD'],
                               realm_name=admin_config['KEYCLOAK_REALM'],
                               verify=True)
