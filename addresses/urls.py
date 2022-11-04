from django.urls import path
from . import views


urlpatterns = [
    path("address/<pk>/", views.UpdateAddressView.as_view()),
]