from rest_framework import generics
from .serializers import AttendanceSerializer, AttendanceDetailSerializer
from .models import Attendance
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import isReceptionist, isDoctor, isOwner

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


class ListAttendancesView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, isDoctor | isOwner]
    serializer_class = AttendanceDetailSerializer
    lookup_url_kwarg = "user_id"

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        user_attendances = Attendance.objects.filter(users__id=user_id)
        return user_attendances

