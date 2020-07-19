from django.shortcuts import render, redirect
from rest_framework import generics, status, response
from rest_framework.permissions import AllowAny
from rest_framework.serializers import Serializer, CharField, ValidationError
from django.conf import settings
from rest_framework.exceptions import NotFound , AuthenticationFailed
from django.http.response import JsonResponse
from keycloak import KeycloakOpenID
from keycloak.exceptions import KeycloakConnectionError , KeycloakError


def url_parser(url , params : dict):
    keys = params.keys()
    new_url = url
    if len(keys):
        new_url += "?"
        for key in keys:
            if type(params[key]) == list:
                new_url += key + "=" + params[key][0] + "&"
            else:
                new_url += key + "=" + params[key] + "&"
    return new_url


class SalutView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return response.Response({"new_token": request.authorization_token, "user": request.authUser})


def redirect_view(request):
    params = request.GET.copy()

    to = params.pop('goto', None)

    if not to:
        return JsonResponse({"detail": NotFound.default_detail},
                            status=NotFound.status_code)

    params['token'] = request.authorization_token
    return redirect(to=url_parser(to[0] , params) , permanent=True)


# def convert_time(timedelta):
#     return 2


# REDIRECT_URL = "localhost:22"
# MAX_TIME = 4
# INIT_VIEW = 'nanna'


# def magic_view(request):

#     params = request.GET.copy()

#     token = params.get('token', None)

#     to = request.build_absolute_uri()

#     params['to'] = to

#     if not token:
#         return redirect(to=REDIRECT_URL, permanent=True, **params)

#     else:
#         time = convert_time(token)
#         if time > MAX_TIME:
#             return JsonResponse({"detail": NotFound.default_detail},
#                                 status=NotFound.status_code)
#         else:
#             init_token = params.get('init', None)

#             if not init_token:
#                 return JsonResponse({"detail": NotFound.default_detail},
#                                     status=NotFound.status_code)
#             else:
#                 try:
#                     user = keycloak_web.userinfo(init_token)
#                     params['userAuth'] = user
#                     params['init'] = init_token

#                     return redirect(INIT_VIEW , **params)

#                 except KeycloakError:
#                     return JsonResponse({"detail": AuthenticationFailed.default_detail},
#                                         status=AuthenticationFailed.status_code)
