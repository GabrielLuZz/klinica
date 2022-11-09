from rest_framework import serializers
from users.models import User
from addresses.serializers import AddressesSerializer
from specialty.serializers import SpecialtySerializer, Specialty


class PatientSerializer(serializers.ModelSerializer):

    address = AddressesSerializer()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "cpf",
            "password",
            "birth_date",
            "is_doctor",
            "last_login",
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
            'password': {'write_only': True},
            "cpf": {"required": True}
        }


    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class DoctorSerializer(serializers.ModelSerializer):
    specialties = SpecialtySerializer(many=True, read_only=True)
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
            "is_receptionist",
            "is_superuser",
            "specialties",
        ]
        read_only_fields = [
            "id",
            "is_receptionist",
            "is_superuser",
        ]
        unique_fields = ["username", "cpf"]
        extra_kwargs = {
            'password': {'write_only': True},
            "cpf": {"required": True},
        }

    def create (self, validated_data):
        specialties_data = validated_data.pop("specialties")
        doctor = User.objects.create_user(**validated_data)


        for specialty in specialties_data:
            specialty, _ = Specialty.objects.get_or_create(**specialty)
            doctor.specialties.add(specialty)
        
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
            "first_name": {"required": True},
            "last_name": {"required": True},
            "cpf": {"required": True}
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