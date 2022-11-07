from django.urls import path
from . import views


urlpatterns = [
    path("clinic/register/", views.CreateClinicView.as_view()),
    path("clinic/", views.ListClinicView.as_view()),
    path("clinic/<pk>/", views.DetailClinicView.as_view()),
]
