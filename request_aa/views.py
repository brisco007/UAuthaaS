from django.shortcuts import render, redirect
from rest_framework import generics, status, response
from rest_framework.permissions import AllowAny
from rest_framework.serializers import Serializer, CharField, ValidationError
from django.conf import settings
from rest_framework.exceptions import NotFound
from django.http.response import JsonResponse
from keycloak import KeycloakOpenID
from keycloak.exceptions import KeycloakConnectionError


class SalutView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return response.Response({"new_token": request.authorization_token, "user": request.authUser})


def redirect_view(request):
    params = request.GET.copy()

    to = params.pop('to', None)

    if not to:
        return JsonResponse({"detail": NotFound.default_detail},
                            status=NotFound.status_code)

    params['token'] = request.authorization_token
    return redirect(to=to[0], permanent=True, **params)