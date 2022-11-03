from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path("patients/", views.UserPatientView.as_view()),
    path("patients/<pk>/", views.UserPatientDetailView.as_view()),
    path("doctor/", views.UserDoctorView.as_view()),
    path("doctor/<pk>/", views.UserDoctorDetailView.as_view()),
    path("recepcionists/", views.UserRecepcionistView.as_view()),
    path("recepcionists/<pk>/", views.UserRecepcionistDetailView.as_view()),
]
