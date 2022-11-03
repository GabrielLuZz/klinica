from rest_framework.permissions import BasePermission
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import Response, status
from users.serializers import PatientSerializer, User
import datetime
from django.contrib.auth.hashers import make_password


class IsReceptionistOrAdm(BasePermission):
    def has_permission(self, request, view):

        SAFE_METHODS = ("GET", "HEAD", "OPTIONS")

        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_superuser
            or request.user.is_receptionist
        )


class IsDoctorOrAdm(BasePermission):
    def has_permission(self, request, view):

        SAFE_METHODS = ("GET", "HEAD", "OPTIONS")

        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_superuser
            or request.user.is_doctor
        )


class LoginPatientUser(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        patient = User.objects.filter(username=request.data["username"])

        patient_serializer = PatientSerializer(patient[0])

        if (
            patient_serializer.data["last_login"] == None
            and "new_password" not in request.data
        ):
            return Response(
                {
                    "detail": "New patients need to send a key new_password to update their password before login"
                },
                status.HTTP_400_BAD_REQUEST,
            )

        if patient_serializer.data["last_login"] == None:

            to_update = {
                "password": make_password(request.data["new_password"]),
                "last_login": datetime.datetime.today(),
            }

            update_patient = PatientSerializer(patient[0], to_update, partial=True)
            update_patient.is_valid(raise_exception=True)
            update_patient.save()

        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})
