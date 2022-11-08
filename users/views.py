from django.shortcuts import render

from utils.helpers import get_object_or_404_with_message
from specialty.models import Specialty
from rest_framework.views import Response, status

from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, DestroyAPIView, UpdateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView

from users.models import User
from users.serializers import (
    DoctorSerializer,
    PatientSerializer,
    ReceptionistSerializer,
)
from utils.patientMixins import AddressSave

from rest_framework.authentication import TokenAuthentication

from utils.specialtiesMixins import SpecialtySave
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


class UserPatientDetailPatchView(UpdateAPIView, DestroyAPIView):

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


    # def create(self, request, *args, **kwargs):
    #     specialties = request.data.pop("specialties")
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
        
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     doctor = User.objects.filter(id=serializer.data["id"])

    #     for specialty in specialties:
    #         specialty, _ = Specialty.objects.get_or_create(**specialty)
    #         doctor.specialties.add(specialty)
        
    #     doctor_serializer = self.get_serializer(doctor)
    #     doctor_serializer.is_valid(raise_exception=True)

    #     return Response(doctor_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        


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
