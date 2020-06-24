"""radius URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from request_aa.views import SalutView, redirect_view
from users_crud.api.views import LoginAPI, SignupAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/login', LoginAPI.as_view()),
    path('users/', include('users_crud.api.urls')),
    path('salut/', SalutView.as_view()),
    path('access/', redirect_view),
    path('auth/signup', SignupAPI.as_view()),
]
