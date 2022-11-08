from django.urls import path
from . import views

urlpatterns = [
    path("attendance/", views.CreateAttendanceView.as_view()),
    path("attendance/<int:attendance_id>/", views.RetrieveUpdateAttendanceView.as_view()),
    path("attendance/<int:user_id>/user/", views.ListAttendancesOwnerView.as_view()),
    path("attendance/<int:user_id>/doctor/", views.ListAttendancesDoctorView.as_view()),
]
