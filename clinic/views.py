from django.shortcuts import render
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from clinic.models import Clinic
from clinic.serializers import ClinicSerializer, ClinicListSerializer
from rest_framework.authentication import TokenAuthentication
from .permissions import isAdminOrReadOnly
from utils.clinic_doctor_mixins import DoctorSave

# Create your views here.


class ListClinicView(ListAPIView):
    queryset = Clinic.objects.all()
    serializer_class = ClinicListSerializer


class CreateClinicView(DoctorSave, CreateAPIView):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [isAdminOrReadOnly]


class DetailClinicView(RetrieveUpdateDestroyAPIView):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer
