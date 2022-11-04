from django.urls import path
from . import views

urlpatterns = [
    path("attendance/", views.CreateAttendanceView.as_view()),
    path("attendance/<attendance_id>/", views.RetrieveUpdateAttendanceView.as_view()),
    path("attendance/<user_id>/user/", views.ListAttendancesOwnerView.as_view()),
    path("attendance/<user_id>/doctor/", views.ListAttendancesDoctorView.as_view()),
]
