import re
import logging
from django.conf import settings
from django.http.response import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from keycloak import KeycloakOpenID
from keycloak.exceptions import KeycloakInvalidTokenError,\
    raise_error_from_response, KeycloakGetError, KeycloakAuthenticationError
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
import json
import datetime
import base64
from .fake import user_authorize

logger = logging.getLogger(__name__)


class AuthorizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        self.config = settings.KEYCLOAK_IAM_CLIENT_CONFIG
        try:
            self.client_id = self.config['KEYCLOAK_CLIENT_ID']
        except KeyError:
            raise Exception(
                "KEYCLOAK_CLIENT_ID not found.")

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        self._config = value

    @property
    def client_id(self):
        return self._client_id

    @client_id.setter
    def client_id(self, value):
        self._client_id = value

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if hasattr(settings, 'KEYCLOAK_USER_AUTHORIZATION_EXEMPT_PATHS'):
            path = request.path_info.lstrip('/')

            if any(re.match(m, path) for m in
                   settings.KEYCLOAK_USER_AUTHORIZATION_EXEMPT_PATHS):
                logger.debug('** exclude path found, skipping')
                return None
        if not hasattr(request, "authUser"):
            return JsonResponse({"detail": NotAuthenticated.default_detail},
                                status=NotAuthenticated.status_code)

        # auth_header = request.META.get('HTTP_AUTHORIZATION').split()
        # token = auth_header[1] if len(auth_header) == 2 else auth_header[0]

        auth_user = request.authUser

        if user_authorize(auth_user):
            authorization_token_str = self.client_id + \
                "&" + datetime.datetime.now().isoformat()
            authorization_token = base64.b64encode(
                authorization_token_str.encode('ascii'))

            request.authorization_token = authorization_token

        else:
            return JsonResponse({"detail": "Vous n'etes pas authorisé. Verifiez vos Forfaits",
            "code" : settings.CUSTOM_ERRORS_TEXT['AUTORIZATION_FAILLED']},
                                status=NotAuthenticated.status_code)

        return None
