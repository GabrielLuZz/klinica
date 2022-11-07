from rest_framework import generics
from .serializers import AttendanceSerializer, AttendanceDetailSerializer
from .models import Attendance
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import isReceptionist, isDoctor, isOwner
<<<<<<< HEAD
=======
from rest_framework.views import Response, status
>>>>>>> 20e9d5f7335a78af56e2799a41767c1fc7491466

# Create your views here.


class CreateAttendanceView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [isReceptionist, IsAuthenticated]
    serializer_class = AttendanceSerializer
    queryset = Attendance.objects


class RetrieveUpdateAttendanceView(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, isDoctor]
    serializer_class = AttendanceDetailSerializer
    queryset = Attendance.objects

    lookup_url_kwarg = "attendance_id"


<<<<<<< HEAD
class ListAttendancesView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, isDoctor | isOwner]
=======
class ListAttendancesOwnerView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, isOwner]
>>>>>>> 20e9d5f7335a78af56e2799a41767c1fc7491466
    serializer_class = AttendanceDetailSerializer
    lookup_url_kwarg = "user_id"

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
<<<<<<< HEAD
        user_attendances = Attendance.objects.filter(users__id=user_id)
        return user_attendances

=======
        user_attendances = Attendance.objects.filter(
            users__id=user_id, users__is_doctor=False, users__is_receptionist=False
        )
        return user_attendances


class ListAttendancesDoctorView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, isDoctor]
    serializer_class = AttendanceDetailSerializer
    lookup_url_kwarg = "user_id"

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        user_attendances = Attendance.objects.filter(
            users__id=user_id, users__is_doctor=True
        )

        return user_attendances
>>>>>>> 20e9d5f7335a78af56e2799a41767c1fc7491466
