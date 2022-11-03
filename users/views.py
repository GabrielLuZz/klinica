from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, DestroyAPIView, UpdateAPIView
from users.models import User
from users.serializers import PatientSerializer
from utils.patientMixins import AddressSave
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from utils.authenticationMixins import IsRecepcionistOrAdm, IsDoctorOrAdm


# Create your views here.
class UserPatientView(ListAPIView):
    
    queryset = User.objects.all()
    serializer_class = PatientSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get_queryset(self):

      return self.queryset.filter(is_doctor=False, is_recepcionist=False, is_superuser=False)

  
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

      return self.queryset.filter(is_doctor=False, is_recepcionist=False, is_superuser=False)



class UserPatientDetailView(RetrieveAPIView):

    queryset = User.objects.all()
    serializer_class = PatientSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsDoctorOrAdm]

    def get_queryset(self):

      return self.queryset.filter(is_doctor=False, is_recepcionist=False, is_superuser=False)
