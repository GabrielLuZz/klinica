from django.shortcuts import render

from utils.helpers import get_object_or_404_with_message
from specialty.models import Specialty
from rest_framework.views import Response, Request, status, APIView

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
from utils.authenticationMixins import IsReceptionistOrAdm, IsDoctorOrAdm, IsDoctorOrAdmOrOwner

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
    permission_classes = [IsDoctorOrAdmOrOwner]

    def get_queryset(self):

        return self.queryset.filter(
            is_doctor=False, is_receptionist=False, is_superuser=False
        )


class UserDoctorView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [isAdminOrReadOnly]

    def get(self, request: Request) -> Response:
        doctors = User.objects.all()
        serializer = DoctorSerializer(many=True, instance=doctors)

        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        specialties_data = request.data.pop("specialties")
        serializer = DoctorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        serializer.save(specialties=specialties_data)

        return Response(serializer.data, status.HTTP_201_CREATED)



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
