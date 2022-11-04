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
            "cpf",
            "password",
            "birth_date",
            "is_doctor",
            "last_login",
            "is_receptionist",
            "address",
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
        unique_fields = ["username", "cpf"]


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
        write_only_fields = ["password"]
        unique_fields = ["username", "cpf"]
