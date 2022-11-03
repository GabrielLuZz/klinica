from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from users.models import User
from users.serializers import (
    DoctorSerializer,
    PatientSerializer,
    RecepcionistSerializer,
)
from utils.patientMixins import AddressSave
from rest_framework.authentication import TokenAuthentication
from permissions import isAdminOrReadOnly

# Create your views here.
class UserPatientView(AddressSave, ListCreateAPIView):

    queryset = User.objects.all()
    serializer_class = PatientSerializer

    def get_queryset(self):

        return self.queryset.filter(
            is_doctor=False, is_recepcionist=False, is_superuser=False
        )


class UserPatientDetailView(RetrieveUpdateDestroyAPIView):

    queryset = User.objects.all()
    serializer_class = PatientSerializer

    def get_queryset(self):

        return self.queryset.filter(
            is_doctor=False, is_recepcionist=False, is_superuser=False
        )


class UserDoctorView(ListCreateAPIView):

    queryset = User.objects.all()
    serializer_class = DoctorSerializer

    def get_queryset(self):

        return self.queryset.filter(
            is_doctor=True, is_recepcionist=False, is_superuser=False
        )


class UserDoctorDetailView(RetrieveUpdateDestroyAPIView):

    queryset = User.objects.all()
    serializer_class = DoctorSerializer

    def get_queryset(self):

        return self.queryset.filter(
            is_doctor=True, is_recepcionist=False, is_superuser=False
        )


class UserRecepcionistView(ListCreateAPIView):

    queryset = User.objects.all()
    serializer_class = RecepcionistSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [isAdminOrReadOnly]

    def get_queryset(self):

        return self.queryset.filter(
            is_doctor=False, is_recepcionist=True, is_superuser=False
        )


class UserRecepcionistDetailView(RetrieveUpdateDestroyAPIView):

    queryset = User.objects.all()
    serializer_class = RecepcionistSerializer

    def get_queryset(self):

        return self.queryset.filter(
            is_doctor=False, is_recepcionist=True, is_superuser=False
        )
