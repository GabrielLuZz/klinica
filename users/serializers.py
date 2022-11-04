from rest_framework import serializers
from users.models import User
from addresses.serializers import AddressesSerializer


class PatientSerializer(serializers.ModelSerializer):

    address = AddressesSerializer()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "cpf",
            "birth_date",
            "is_doctor",
            "is_receptionist",
            "address",
            "last_login",
        ]
        read_only_fields = [
            "id",
            "is_doctor",
            "is_receptionist",
            "is_superuser",
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }


    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "cpf",
            "birth_date",
            "is_doctor",
            "crm",
            "clinic",
            "is_receptionist",
            "is_superuser",
        ]
        read_only_fields = [
            "id",
            "is_receptionist",
            "is_superuser",
        ]
        unique_fields = ["username", "cpf"]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create (self, validated_data):
        doctor = User.objects.create_user(**validated_data)
        return doctor


class ReceptionistSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "cpf",
            "birth_date",
            "is_doctor",
            "is_receptionist",
        ]
        read_only_fields = ["id"]
        unique_fields = ["username", "cpf"]
        extra_kwargs = {
            'password': {'write_only': True},
            "is_receptionist": {"default": True},
        }

    def create (self, validated_data):
        return User.objects.create_user(**validated_data)

class DoctorAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "cpf",
            "is_doctor",
        ]

class ReceptionistAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "cpf",
            "is_receptionist",
        ]

class PatientAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "cpf",
        ]