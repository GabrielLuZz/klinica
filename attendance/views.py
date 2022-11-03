from rest_framework import generics
from .serializers import AttendanceSerializer, AttendanceDetailSerializer
from .models import Attendance
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class ListCreateAttendanceView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = AttendanceSerializer
    queryset = Attendance.objects