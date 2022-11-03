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
            "birth_date",
            "is_doctor",
            "is_receptionist",
            "address",
        ]
        read_only_fields = [
            "id",
            "is_doctor",
            "is_receptionist",
            "is_superuser",
        ]
        write_only_fields = ["password"]
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
            "email",
            "cpf",
            "birth_date",
            "is_doctor",
            "crm",
            "clinic",
        ]
        read_only_fields = ["id"]
        write_only_fields = ["password"]
        unique_fields = ["username", "cpf"]


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
