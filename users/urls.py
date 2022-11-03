from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path("patients/", views.UserPatientView.as_view()),
    path("patients/<pk>/", views.UserPatientDetailView.as_view()),
]