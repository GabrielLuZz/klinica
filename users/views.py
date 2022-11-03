from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, DestroyAPIView, UpdateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from users.models import User
from users.serializers import (
    DoctorSerializer,
    PatientSerializer,
    RecepcionistSerializer,
)
from utils.patientMixins import AddressSave

from rest_framework.authentication import TokenAuthentication
from .permissions import isAdminOrReadOnly
from rest_framework.permissions import IsAdminUser
from utils.authenticationMixins import IsRecepcionistOrAdm, IsDoctorOrAdm

# Create your views here.
class UserPatientView(ListAPIView):
    
    queryset = User.objects.all()
    serializer_class = PatientSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get_queryset(self):

      return self.queryset.filter(is_doctor=False, is_receptionist=False, is_superuser=False)

  
class UserPatientCreateView(AddressSave, CreateAPIView):
    
    queryset = User.objects.all()
    serializer_class = PatientSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsRecepcionistOrAdm]


class UserPatientDetailView(UpdateAPIView, DestroyAPIView):

    queryset = User.objects.all()
    serializer_class = PatientSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsRecepcionistOrAdm]

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


class UserRecepcionistView(ListCreateAPIView):

    queryset = User.objects.all()
    serializer_class = RecepcionistSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [isAdminOrReadOnly]

    def get_queryset(self):

        return self.queryset.filter(
            is_doctor=False, is_receptionist=True, is_superuser=False
        )


class UserRecepcionistDetailView(RetrieveUpdateDestroyAPIView):

    queryset = User.objects.all()
    serializer_class = RecepcionistSerializer

    def get_queryset(self):

        return self.queryset.filter(
            is_doctor=False, is_receptionist=True, is_superuser=False
        )
