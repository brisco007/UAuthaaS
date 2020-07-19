#biling urls, and from #, we have localhost/biling/here
from django.urls import include, path
from rest_framework import routers
from . import views


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('forfaits/', views.ForfaitView.as_view()),
    path('comptes_users/',views.CompteUserView.as_view()),
    path('forfaits/<uuid:id>/',views.ForfaitDetailsView.as_view()),
    path('comptes_users/<uuid:id>/',views.CompteUserDetailsView.as_view()),
    path('comptes_users_user/<uuid:userid>/',views.CompteUserDetailsUserView.as_view())
]