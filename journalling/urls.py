#journalling urls, and from #, we have localhost/journal/here
from django.urls import include, path
from rest_framework import routers
from . import views

urlpatterns = [
    path('journals/', views.JournalView.as_view()),
    path('journals/<uuid:id>/',views.JournalDetailsView.as_view()),
]