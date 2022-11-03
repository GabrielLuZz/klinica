from django.shortcuts import render

from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, DestroyAPIView, UpdateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView

from users.models import User
from users.serializers import (
    DoctorSerializer,
    PatientSerializer,
    ReceptionistSerializer,
)
from utils.patientMixins import AddressSave

from rest_framework.authentication import TokenAuthentication
from .permissions import isAdminOrReadOnly
from rest_framework.permissions import IsAdminUser
from utils.authenticationMixins import IsReceptionistOrAdm, IsDoctorOrAdm

# Create your views here.
class UserPatientView(ListAPIView):

    queryset = User.objects.all()
    serializer_class = PatientSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get_queryset(self):

        return self.queryset.filter(
            is_doctor=False, is_receptionist=False, is_superuser=False
        )

class UserPatientCreateView(AddressSave, CreateAPIView):

    queryset = User.objects.all()
    serializer_class = PatientSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsReceptionistOrAdm]


class UserPatientDetailView(UpdateAPIView, DestroyAPIView):

    queryset = User.objects.all()
    serializer_class = PatientSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsReceptionistOrAdm]

    def get_queryset(self):

        return self.queryset.filter(
            is_doctor=False, is_receptionist=False, is_superuser=False
        )


class UserPatientDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = PatientSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsDoctorOrAdm]

    def get_queryset(self):

        return self.queryset.filter(
            is_doctor=False, is_receptionist=False, is_superuser=False
        )


class UserDoctorView(ListCreateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [isAdminOrReadOnly]

    queryset = User.objects.all()
    serializer_class = DoctorSerializer

    def get_queryset(self):

        return self.queryset.filter(
            is_doctor=True, is_receptionist=False, is_superuser=False
        )


class UserDoctorDetailView(RetrieveUpdateDestroyAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [isAdminOrReadOnly]

    queryset = User.objects.all()
    serializer_class = DoctorSerializer

    def get_queryset(self):

        return self.queryset.filter(
            is_doctor=True, is_receptionist=False, is_superuser=False
        )


class UserReceptionistView(ListCreateAPIView):

    queryset = User.objects.all()
    serializer_class = ReceptionistSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [isAdminOrReadOnly]

    def get_queryset(self):

        return self.queryset.filter(
            is_doctor=False, is_receptionist=True, is_superuser=False
        )


class UserReceptionistDetailView(RetrieveUpdateDestroyAPIView):

    queryset = User.objects.all()
    serializer_class = ReceptionistSerializer

    def get_queryset(self):

        return self.queryset.filter(
            is_doctor=False, is_receptionist=True, is_superuser=False
        )
