from rest_framework import serializers
from .models import Clinic
from users.models import User


class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = ["id", "clinic_name", "is_ocuped", "is_ok", "doctor"]
        read_only_fields = ["id"]


class DoctorReturn(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "crm", "specialties"]
        read_only_fields = ["id"]


class ClinicListSerializer(serializers.ModelSerializer):

    doctor = DoctorReturn()

    class Meta:
        model = Clinic
        fields = ["id", "clinic_name", "is_ocuped", "is_ok", "doctor"]
        read_only_fields = ["id"]
