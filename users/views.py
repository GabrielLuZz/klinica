from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from users.models import User
from users.serializers import DoctorSerializer, PatientSerializer
from utils.patientMixins import AddressSave
# Create your views here.
class UserPatientView(AddressSave, ListCreateAPIView):
    
    queryset = User.objects.all()
    serializer_class = PatientSerializer

    def get_queryset(self):

      return self.queryset.filter(is_doctor=False, is_recepcionist=False, is_superuser=False)


class UserPatientDetailView(RetrieveUpdateDestroyAPIView):    

    queryset = User.objects.all()
    serializer_class = PatientSerializer

    def get_queryset(self):

      return self.queryset.filter(is_doctor=False, is_recepcionist=False, is_superuser=False)


class UserDoctorView(ListCreateAPIView):
    
    queryset = User.objects.all()
    serializer_class = DoctorSerializer

    def get_queryset(self):

      return self.queryset.filter(is_doctor=True, is_recepcionist=False, is_superuser=False)


class UserDoctorDetailView(RetrieveUpdateDestroyAPIView):    

    queryset = User.objects.all()
    serializer_class = DoctorSerializer

    def get_queryset(self):

      return self.queryset.filter(is_doctor=True, is_recepcionist=False, is_superuser=False)
