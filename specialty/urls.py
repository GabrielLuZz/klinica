from django.urls import path
from . import views


urlpatterns = [
    path("specialty/", views.ListSpecialtyView.as_view()),
    path("specialty/create/", views.CreateSpecialtyView.as_view()),
    path("specialty/<pk>/", views.DetailSpecialtyView.as_view()),
]