from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from utils.authenticationMixins import LoginPatientUser


urlpatterns = [
    path("patients/register/", views.UserPatientCreateView.as_view()),
    path("patients/", views.UserPatientView.as_view()),
    path("patients/<pk>/", views.UserPatientDetailView.as_view()),
    path("patient/<pk>/", views.UserPatientDetailPatchView.as_view()),
    path("login/", obtain_auth_token),
    path("login/patient/", LoginPatientUser.as_view()),
    path("doctor/", views.UserDoctorView.as_view()),
    path("doctor/<pk>/", views.UserDoctorDetailView.as_view()),
    path("receptionists/", views.UserReceptionistView.as_view()),
    path("receptionists/<pk>/", views.UserReceptionistDetailView.as_view()),
]
